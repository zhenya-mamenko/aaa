export interface Category {
  /*
  Interface representing an asset category.

  Attributes:
    category_id (number | null): The ID of the asset category.
    class_id (number): The ID of the asset class.
    category_name (string): The name of the asset category.
  */
  category_id?: number | null;
  class_id: number;
  category_name: string;
}

export interface CategoryResponse {
  /*
  Response interface for an asset category.

  Attributes:
    category_id (number): The ID of the category.
    class_id (number): The ID of the class.
    class_name (string): The name of the class.
    category_name (string): The name of the category.
  */
  category_id: number;
  class_id: number;
  class_name: string;
  category_name: string;
}
