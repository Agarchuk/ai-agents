from langgraph.graph import StateGraph, END

from backend.models.pydantic.duplicates.duplicates_recommendations import DuplicatesRecommendations
from backend.nodes import dataset_topic_node
from backend.nodes.dataset_topic_node import DatasetTopicNode
from backend.states.cleaning_agent_state import CleaningAgentState
from backend.nodes.analysis_node import AnalysisNode
from backend.nodes.missing_values.missing_values_node import MissingValuesNode
from backend.nodes.missing_values.handle_missing_values_node import HandleMissingValuesNode
from backend.nodes.duplicates.duplicate_values_node import DuplicateValuesNode
from backend.nodes.duplicates.handle_duplicate_values_node import HandleDuplicateValuesNode
from backend.nodes.outliers.detect_outliers_node import DetectOutliersNode
from backend.nodes.handle_outliers_node import HandleOutliersNode
from backend.models.pydantic.outliers_info import OutliersInfo
from backend.nodes.outliers.handle_plausibility_of_outliers_node import HandlePlausibilityOfOutliersNode
from utils.logger import log_info
from backend.nodes.human_confirmation_node import HumanConfirmationNode

class CleaningAgent:
    def __init__(self, 
                 dataset_topic_node: DatasetTopicNode,
                 analysis_node: AnalysisNode, 
                 missing_values_node: MissingValuesNode, 
                 handle_missing_values_node: HandleMissingValuesNode, 
                 duplicate_values_node: DuplicateValuesNode, 
                 handle_duplicate_values_node: HandleDuplicateValuesNode, 
                 detect_outliers_node: DetectOutliersNode,
                 handle_plausibility_of_outliers_node: HandlePlausibilityOfOutliersNode,
                 human_confirmation_node: HumanConfirmationNode):
        self.dataset_topic_node: DatasetTopicNode = dataset_topic_node
        self.analysis_node: AnalysisNode = analysis_node  
        self.missing_values_node: MissingValuesNode = missing_values_node
        self.handle_missing_values_node: HandleMissingValuesNode = handle_missing_values_node
        self.duplicate_values_node: DuplicateValuesNode = duplicate_values_node
        self.handle_duplicate_values_node: HandleDuplicateValuesNode = handle_duplicate_values_node
        self.detect_outliers_node: DetectOutliersNode = detect_outliers_node
        self.handle_plausibility_of_outliers_node: HandlePlausibilityOfOutliersNode = handle_plausibility_of_outliers_node
        self.human_confirmation_node = human_confirmation_node
        # self.handle_outliers_node: HandleOutliersNode = handle_outliers_node
        
        self.agent = self._build_workflow()

        try:
            log_info(f"Agent graph: {self.agent.get_graph()}")
            self.agent.get_graph().draw_png("cleaning_agent.png")
            self.agent.get_graph().draw_mermaid_png(output_file_path="cleaning_agent_workflow.png")
        except Exception as e:
            print(f"Failed to visualize workflow graph: {str(e)}")
            print("Agent will continue working without visualization.")

    def _build_workflow(self):
        workflow = StateGraph(CleaningAgentState)
        
        workflow.add_node("dataset_topic_node", self.dataset_topic_node.get_topic_from_llm)
        workflow.add_node("analyze_data", self.analysis_node.analyze_data)
        workflow.add_node("missing_values_node", self.missing_values_node.process_missing_values)
        workflow.add_node("handle_missing_values", self.handle_missing_values_node.process_missing_values)
        workflow.add_node("duplicate_values_node", self.duplicate_values_node.detect_duplicate_values)
        workflow.add_node("handle_duplicate_values", self.handle_duplicate_values_node.handle_duplicate_values)
        workflow.add_node("detect_outliers", self.detect_outliers_node.detect_outliers)
        workflow.add_node("handle_plausibility_of_outliers", self.handle_plausibility_of_outliers_node.handle_plausibility_of_outliers)

        workflow.add_edge("dataset_topic_node", "analyze_data")
        workflow.add_conditional_edges(
            "analyze_data",
            self.missing_values_condition,
            {
                "process_missing_values": "missing_values_node",
                "duplicate_values_node": "duplicate_values_node"
            }
        )
        workflow.add_edge("missing_values_node", "handle_missing_values")
        workflow.add_edge("handle_missing_values", "duplicate_values_node")

        workflow.add_conditional_edges(
            "duplicate_values_node",
            self.duplicate_values_condition,
            {
                "handle_duplicate_values": "handle_duplicate_values",
                "detect_outliers": "detect_outliers"
            }
        )
        workflow.add_edge("handle_duplicate_values", "detect_outliers")
        
        workflow.add_conditional_edges(
            "detect_outliers",
            self.outliers_condition,
            {
                "handle_plausibility_of_outliers": "handle_plausibility_of_outliers",
                END: END
            }
        )
        workflow.add_edge("handle_plausibility_of_outliers", END)
        
        workflow.set_entry_point("dataset_topic_node")
        return workflow.compile()
    
    def invoke(self, state: CleaningAgentState) -> CleaningAgentState:
        return self.agent.invoke(state)
    
    def missing_values_condition(self, state: CleaningAgentState):
        if state.report.missing_values.sum() > 0:
            return "process_missing_values"
        return "duplicate_values_node"
    
    def duplicate_values_condition(self, state: CleaningAgentState):
        duplicates_recommendations: DuplicatesRecommendations = state.report.duplicates_recommendations
        if duplicates_recommendations.duplicates_recommendations:
            return "handle_duplicate_values"
        return "detect_outliers"
    
    def outliers_condition(self, state: CleaningAgentState):
        detected_outliers: OutliersInfo = state.report.detected_outliers
        if detected_outliers:
            log_info(f"detected_outliers: {detected_outliers}")
            return "handle_plausibility_of_outliers"
        return END

    def human_confirmation_condition(self, state: CleaningAgentState):
        return "dataset_topic_node" if state.continue_cleaning else END