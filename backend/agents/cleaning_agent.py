from langgraph.graph import StateGraph, END

from backend.agents.nodes import detect_outliers_node
from backend.agents.states.cleaning_agent_state import CleaningAgentState
from backend.agents.nodes.analysis_node import AnalysisNode
from backend.agents.nodes.missing_values_node import MissingValuesNode
from backend.agents.nodes.handle_missing_values_node import HandleMissingValuesNode
from backend.agents.nodes.duplicate_values_node import DuplicateValuesNode
from backend.agents.nodes.handle_duplicate_values_node import HandleDuplicateValuesNode
from backend.agents.nodes.detect_outliers_node import DetectOutliersNode
from backend.agents.nodes.handle_outliners_node import HandleOutlinersNode
from backend.models.pydantic.duplicates_analysis import DuplicatesAnalysis
from IPython.display import Image, display
from backend.models.pydantic.outliers_info import OutliersInfo

class CleaningAgent:
    def __init__(self, analysis_node: AnalysisNode, missing_values_node: MissingValuesNode, handle_missing_values_node: HandleMissingValuesNode, duplicate_values_node: DuplicateValuesNode, handle_duplicate_values_node: HandleDuplicateValuesNode, detect_outliners_node: DetectOutliersNode, handle_outliners_node: HandleOutlinersNode):
        self.analysis_node: AnalysisNode = analysis_node  
        self.missing_values_node: MissingValuesNode = missing_values_node
        self.handle_missing_values_node: HandleMissingValuesNode = handle_missing_values_node
        self.duplicate_values_node: DuplicateValuesNode = duplicate_values_node
        self.handle_duplicate_values_node: HandleDuplicateValuesNode = handle_duplicate_values_node
        self.detect_outliners_node: DetectOutliersNode = detect_outliners_node
        self.handle_outliners_node: HandleOutlinersNode = handle_outliners_node
        self.agent = self._build_workflow()
        graph_image = self.agent.get_graph().draw_mermaid_png()
        with open("cleaning_agent_workflow.png", "wb") as f:
            f.write(graph_image)
        display(Image(graph_image))

    def _build_workflow(self):
        workflow = StateGraph(CleaningAgentState)

        workflow.add_node("analyze_data", self.analysis_node.analyze_data)
        workflow.add_node("missing_values_node", self.missing_values_node.process_missing_values)
        workflow.add_node("handle_missing_values", self.handle_missing_values_node.process_missing_values)
        workflow.add_node("duplicate_values_node", self.duplicate_values_node.detect_duplicate_values)
        workflow.add_node("handle_duplicate_values", self.handle_duplicate_values_node.handle_duplicate_values)
        workflow.add_node("detect_outliners", self.detect_outliners_node.detect_outliners)
        workflow.add_node("handle_outliners", self.handle_outliners_node.handle_outliners)

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
                "detect_outliners": "detect_outliners"
            }
        )
        workflow.add_edge("handle_duplicate_values", "detect_outliners")
        workflow.add_conditional_edges(
            "detect_outliners",
            self.outliers_condition,
            {
                "handle_outliners": "handle_outliners",
                END: END
            }
        )
        workflow.add_edge("handle_outliners", END)
        workflow.set_entry_point("analyze_data")
        return workflow.compile()
    
    def invoke(self, state: CleaningAgentState) -> CleaningAgentState:
        return self.agent.invoke(state)
    
    def missing_values_condition(self, state: CleaningAgentState):
        if state["analysis"].missing_values.sum() > 0:
            return "process_missing_values"
        return "duplicate_values_node"
    
    def duplicate_values_condition(self, state: CleaningAgentState):
        duplicates_analysis: DuplicatesAnalysis = state["duplicates_analysis"]
        if duplicates_analysis.unique_identifier_column or duplicates_analysis.combined_key_columns:
            return "handle_duplicate_values"
        return "detect_outliners"
    
    def outliers_condition(self, state: CleaningAgentState):
        outliers_info: OutliersInfo = state["outliers_info"]
        if outliers_info:
            return "handle_outliners"
        return END
