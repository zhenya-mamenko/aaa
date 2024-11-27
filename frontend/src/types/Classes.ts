export interface Class {
  /*
  Interface representing an asset class.

  Attributes:
    class_id (number | null): The ID of the asset class.
    class_name (string): The name of the asset class.
  */
  class_id?: number | null;
  class_name: string;
}


export interface ClassResponse {
  /*
  Response interface for an asset class.

  Attributes:
    class_id (number): The ID of the class.
    class_name (string): The name of the class.
  */
  class_id: number;
  class_name: string;
}
