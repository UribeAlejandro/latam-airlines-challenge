# Solution

## Part I

In order to operationalize the model, transcribe the `.ipynb` file into the `model.py` file:

- If you find any bug, fix it.
- The DS proposed a few models in the end. Choose the best model at your discretion, argue why. **It is not necessary to make improvements to the model.**
- Apply all the good programming practices that you consider necessary in this item.
- The model should pass the tests by running `make model-test`.

> **Note:**
> - **You cannot** remove or change the name or arguments of **provided** methods.
> - **You can** change/complete the implementation of the provided methods.
> - **You can** create the extra classes and methods you deem necessary.

### Bugs

The following bugs were found in the provided code:

1. In the `get_period_day` function, there were boundary conditions that were not correctly handled. The original logic used `>` and `<` operators, which excluded the exact boundary times (e.g., 5:00, 12:00, 19:00). The corrected logic uses `>=` and `<` to include the boundary times in the appropriate periods. Note that the function has changes in comparison to enhance readability and maintainability, but the core logic remains the same.
2. The `is_high_season` function, had no bugs.
3. The `get_min_diff` function, had no bugs.
4. The `get_rate_from_column` function, had a bug in the calculation of the delay rates. The original code computes the rate as follows:

```python
total / delays[name]
```

But in order to calculate the delay rate, it should be the inverse of that, which is:

```python
delays[name] / total
```

Finally, to express it as a percentage, it is multiplied by 100. The corrected code is:

```python
rates[name] = round(100 * delays[name] / total, 2)
```

### Data

The following suggestions can be considered to improve the data management and preprocessing:

#### Data Preprocessing

A separated class is proposed. It should handle all the data preprocessing steps, this will help to keep the code organized and maintainable. On the other hand, most of the functions found in the [EDA Notebook](../notebooks/exploration.ipynb) are stateless, so they do not require to be methods of a class, they can be implemented as standalone functions in a separate module (i.e., [etl.py](../challenge/data/etl.py)). This will allow for better separation of concerns and make the code easier to test and maintain.

> A set of tests should be implemented to ensure that the data preprocessing steps are working correctly. Also, to improve the coverage percentage.

#### Data Version Control

To ensure that the data is properly versioned and can be easily accessed and updated, it is recommended using a data version control system such as [DVC](https://dvc.org/). This will allow data practitioners to track changes to the data, collaborate with other team members, and ensure that the interested parties are always working with the most up-to-date version of the data.

### Model Selection

No improvements/changes were introduced in the model selection process. Instead, [MLFlow](https://mlflow.org/) was proposed to be used for tracking experiments, this will allow us to keep track of different model versions, hyperparameters, and performance metrics in a systematic way. The tool at hand facilitates the experimentation, comparison, and deployment of machine learning models, making it easier to manage the model development lifecycle. Please refer to the [Model Selection Notebook](../notebooks/model_selection.ipynb) for more details on the model selection process and the use of MLFlow for experiment tracking.

- Experiment Tracking: using `mlflow.autolog()` to automatically log parameters, metrics, and models during training. Also, evaluation data was included to log the performance of the model on a validation set, enabling MLFlow automatic logging of the evaluation metrics (e.g., accuracy, precision, recall, F1-score) for the validation data, as well as including the plots generated and the model artifacts (e.g., model weights, feature importance plots) in the MLFlow tracking system.

- Model Selection/Promotion: MLFlow allows data practitioners to compare different models and their performance metrics in a systematic way. The MLFlow UI facilitates the comparison of different runs, analysis of the performance of different models, and selection of the best-performing model based on the evaluation metrics. Once the best model has been selected, it can be promoted to production using MLFlow's model registry, which provides versioning and deployment capabilities.

- Model Serving: MLFlow provides a model registry that allows data practitioners to manage and deploy models in a systematic way. Trained models can be registered in the MLFlow model registry, which provides versioning, stage transitions (e.g., staging, production), and deployment capabilities. This will allow us to easily deploy our models to production environments and manage different versions of the models effectively.
