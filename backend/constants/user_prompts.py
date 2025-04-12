

RECOMMEND_CONSTANT_FOR_MISSING_VALUES_USER_PROMPT = (
    """
    The dataset topic is: {dataset_topic}.
    The column '{column_name}' has the following characteristics:
    - Data type: {data_type}
    - Missing values: {missing_percentage}%
    - Statistics: {statistics}

    Recommend a suitable constant to fill the missing values in '{column_name}' and explain why this constant is appropriate.
    """
)
