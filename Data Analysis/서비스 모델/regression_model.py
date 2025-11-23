import numpy as np
import pandas as pd

class DepreciationModel:
    """
    A regression model to estimate the remaining value of a refurbished product
    based on a time-based depreciation formula.
    """
    def __init__(self, category_discount_rates, condition_multipliers):
        """
        Initializes the model with its parameters (weights).

        Args:
            category_discount_rates (dict): A dict mapping product categories to their
                                            base average monthly discount rate.
                                            e.g., {'phone': 0.03, 'laptop': 0.025}
            condition_multipliers (dict): A dict mapping condition grades to a
                                          multiplier for the discount rate.
                                          e.g., {'A': 1.0, 'B': 1.2, 'C': 1.5}
        """
        self.category_rates = category_discount_rates
        self.condition_weights = condition_multipliers

    def predict_value(self, initial_price, category, age_in_months, condition):
        """
        Predicts the remaining value of a single product.

        Args:
            initial_price (float): The original price of the product when new.
            category (str): The product's category (e.g., 'phone').
            age_in_months (int): The age of the product in months.
            condition (str): The condition grade of the product (e.g., 'A', 'B').

        Returns:
            float: The estimated remaining value of the product.
        """
        # 1. Get the base discount rate for the category
        base_rate = self.category_rates.get(category)
        if base_rate is None:
            raise ValueError(f"Unknown category: '{category}'. No discount rate available.")

        # 2. Get the weight/multiplier for the condition
        condition_multiplier = self.condition_weights.get(condition)
        if condition_multiplier is None:
            raise ValueError(f"Unknown condition: '{condition}'. No multiplier available.")
        
        # 3. Calculate the effective discount rate
        effective_discount_rate = base_rate * condition_multiplier

        # 4. Apply the exponential decay formula
        # Value = Initial_Price * (1 - Discount_Rate)^age
        remaining_value = initial_price * ((1 - effective_discount_rate) ** age_in_months)

        return max(0, remaining_value) # Value cannot be negative

if __name__ == '__main__':
    # --- 1. Define the Model Parameters ("weights") ---
    # Average monthly depreciation rate for each category
    avg_discount_rates = {
        'phone': 0.035,  # Phones depreciate at 3.5% per month
        'laptop': 0.025, # Laptops depreciate at 2.5% per month
        'tablet': 0.028, # Tablets depreciate at 2.8% per month
        'watch': 0.020,  # Watches hold value better
    }

    # Condition weights that multiply the discount rate
    condition_multipliers = {
        'A': 1.0,  # Grade A (Excellent): Standard depreciation
        'B': 1.25, # Grade B (Good): Depreciates 25% faster
        'C': 1.60, # Grade C (Fair): Depreciates 60% faster
    }

    # --- 2. Initialize the Model ---
    value_model = DepreciationModel(
        category_discount_rates=avg_discount_rates,
        condition_multipliers=condition_multipliers
    )
    print("Depreciation model initialized with custom rates and weights.")

    # --- 3. Create Sample Data Sets ---
    # This represents products from various sources or data sets
    products_to_evaluate = [
        {'id': 'P001', 'category': 'phone', 'name': 'Galaxy S21', 'initial_price': 1000, 'age_in_months': 12, 'condition': 'A'},
        {'id': 'P002', 'category': 'phone', 'name': 'Galaxy S21', 'initial_price': 1000, 'age_in_months': 12, 'condition': 'C'},
        {'id': 'L001', 'category': 'laptop', 'name': 'MacBook Pro 14', 'initial_price': 2000, 'age_in_months': 24, 'condition': 'A'},
        {'id': 'L002', 'category': 'laptop', 'name': 'Dell XPS 15', 'initial_price': 1800, 'age_in_months': 36, 'condition': 'B'},
        {'id': 'W001', 'category': 'watch', 'name': 'Apple Watch 8', 'initial_price': 400, 'age_in_months': 6, 'condition': 'A'},
    ]
    
    print("\n--- 4. Estimating Remaining Value for Products ---")
    
    results = []
    for product in products_to_evaluate:
        estimated_value = value_model.predict_value(
            initial_price=product['initial_price'],
            category=product['category'],
            age_in_months=product['age_in_months'],
            condition=product['condition']
        )
        product['estimated_value'] = round(estimated_value, 2)
        results.append(product)
        
    # Display results in a structured way using pandas DataFrame
    results_df = pd.DataFrame(results)
    print(results_df[['id', 'name', 'category', 'initial_price', 'age_in_months', 'condition', 'estimated_value']].to_string())

    print("\n--- Interpretation ---")
    print("The model estimates the remaining value based on a starting price, and applies a monthly 'discount' that is")
    print("adjusted based on the product's category and condition.")
    print("For example, notice the two Galaxy S21 phones: the 'Grade C' item has a much lower estimated value than")
    print("the 'Grade A' item, despite being the same age, because its effective discount rate is higher.")
