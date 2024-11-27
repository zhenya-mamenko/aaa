from app.models.base import BaseModel


class PortfolioResponse(BaseModel):
    """
    Response model for a portfolio.

    Attributes:
        category_id (int): The ID of the category.
        class_name (str): The name of the class.
        category_name (str): The name of the category.
        structure_percentile (int): The percentile of category's assets in the structure of asset allocation.
        out_structure_percentile (str): The output for the structure percentile.
        amount (int): The amount of the asset value in cents.
        out_amount (str): The output for the amount.
        total (int): The total amount of all last values in cents.
        out_total (str): The output for the total amount.
        current_percentile (int): The current percentile of category's assets in the structure of asset allocation.
        out_current_percentile (str): The output for the current percentile.
    """
    category_id: int
    class_name: str
    category_name: str
    structure_percentile: int
    out_structure_percentile: str
    amount:int
    out_amount: str
    total: int
    out_total: str
    current_percentile: int
    out_current_percentile: str


__all__ = [
    "PortfolioResponse",
]
