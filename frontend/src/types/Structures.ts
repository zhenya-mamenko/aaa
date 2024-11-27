export interface Structure {
  /*
  Interface representing a structure of asset allocation.

  Attributes:
    structure_id (number | null): The ID of the structure.
    structure_date (string): The date of the structure (for reference only).
    structure_name (string): The name of the structure.
    is_current (boolean): Whether the structure is currently in use.
  */
  structure_id?: number | null;
  structure_date: string;
  structure_name: string;
  is_current: boolean;
}


export interface StructureCategory {
  /*
  Interface representing a category in the structure of asset allocation.

  Attributes:
    structure_id (number): The ID of the structure.
    category_id (number): The ID of the category.
    percentile (number): The percentile of category's assets in the structure of asset allocation.
  */
  structure_id: number;
  category_id: number;
  percentile: number;
}


export interface StructureResponse {
  /*
  Response interface representing a structure of asset allocation.

  Attributes:
    structure_id (number): The ID of the structure.
    structure_date (string): The date of the structure (for reference only).
    structure_name (string): The name of the structure.
    is_current (boolean): Whether the structure is currently in use.
  */
  structure_id: number;
  structure_date: string;
  structure_name: string;
  is_current: boolean;
}


export interface StructureCategoryResponse {
  /*
  Response interface for a structure category.

  Attributes:
    structure_id (number): The ID of the structure.
    category_id (number): The ID of the category.
    class_name (string): The name of the class.
    category_name (string): The name of the category.
    percentile (number): The percentile of category's assets in the structure of asset allocation.
    out_percentile (string): The output for the percentile.
  */
  structure_id: number;
  category_id: number;
  class_name: string;
  category_name: string;
  percentile: number;
  out_percentile: string;
}
