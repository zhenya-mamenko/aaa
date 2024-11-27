export interface PortfolioResponse {
  /*
  Response interface for a portfolio.

  Attributes:
    category_id (number): The ID of the category.
    class_name (string): The name of the class.
    category_name (string): The name of the category.
    structure_percentile (number): The percentile of category's assets in the structure of asset allocation.
    out_structure_percentile (string): The output for the structure percentile.
    amount (number): The amount of the asset value in cents.
    out_amount (string): The output for the amount.
    total (number): The total amount of all last values in cents.
    out_total (string): The output for the total amount.
    current_percentile (number): The current percentile of category's assets in the structure of asset allocation.
    out_current_percentile (string): The output for the current percentile.
  */
  category_id: number;
  class_name: string;
  category_name: string;
  structure_percentile: number;
  out_structure_percentile: string;
  amount: number;
  out_amount: string;
  total: number;
  out_total: string;
  current_percentile: number;
  out_current_percentile: string;
}
