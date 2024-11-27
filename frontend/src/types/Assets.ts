export interface Asset {
  /*
  Interface representing an asset.

  Attributes:
    asset_id (number | null): The ID of the asset.
    category_id (number): The ID of the asset category.
    asset_name (string): The name of the asset.
    asset_ticker (string): The asset_ticker of the asset.
  */
  asset_id?: number | null;
  category_id: number;
  asset_name: string;
  asset_ticker: string;
}

export interface AssetValue {
  /*
  Interface representing the value of an asset.

  Attributes:
    value_datetime (string): The datetime of taking the asset value.
    asset_id (number): The ID of the asset.
    amount (number): The amount of the asset value in cents.
  */
  value_datetime?: string | null;
  asset_id: number;
  amount: number;
}


export interface AssetResponse {
  /*
  Response interface for an asset.

  Attributes:
    asset_id (number): The ID of the asset.
    category_id (number): The ID of the category.
    class_name (string): The name of the class.
    category_name (string): The name of the category.
    asset_name (string): The name of the asset.
    asset_ticker (string): The asset_ticker of the asset.
  */
  asset_id: number;
  category_id: number;
  class_name: string;
  category_name: string;
  asset_name: string;
  asset_ticker: string;
}


export interface AssetsStateResponse {
  /*
  Response interface for the state of assets.

  Attributes:
    asset_id (number): The ID of the asset.
    class_name (string): The name of the class.
    category_name (string): The name of the category.
    asset_name (string): The name of the asset.
    asset_ticker (string): The asset_ticker of the asset.
    last (number): The last amount of the asset value in cents.
    lag (number): The lag (previous of the last) amount of the asset value in cents.
    first (number): The first amount of the asset value in cents.
    last_lag_percent (number): The percentage change from last to lag.
    last_first_percent (number): The percentage change from last to first.
    lag_first_percent (number): The percentage change from lag to first.
    out_last (string): The output for the last value.
    out_lag (string): The output for the lag value.
    out_first (string): The output for the first value.
    out_last_lag_percent (string): The output for the percentage change from last to lag.
    out_last_first_percent (string): The output for the percentage change from last to first.
    out_lag_first_percent (string): The output for the percentage change from lag to first.
  */
  asset_id: number;
  class_name: string;
  category_name: string;
  asset_name: string;
  asset_ticker: string;
  last: number;
  lag: number;
  first: number;
  last_lag_percent: number;
  last_first_percent: number;
  lag_first_percent: number;
  out_last: string;
  out_lag: string;
  out_first: string;
  out_last_lag_percent: string;
  out_last_first_percent: string;
  out_lag_first_percent: string;
}


export interface AssetsValuesResponse {
  /*
  Response interface for the values of assets.

  Attributes:
    asset_id (number): The ID of the asset.
    class_name (string): The name of the class.
    category_name (string): The name of the category.
    asset_name (string): The name of the asset.
    asset_ticker (string): The asset_ticker of the asset.
    asset_value_datetime (string): The datetime of taking the asset value.
    amount (number): The amount of the asset value in cents.
    out_amount (string): The output for the amount.
  */
  asset_id: number;
  class_name: string;
  category_name: string;
  asset_name: string;
  asset_ticker: string;
  asset_value_datetime: string;
  amount: number;
  out_amount: string;
}
