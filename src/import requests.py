import requests
import pandas as pd
import os

BASE_URL = "https://fakestoreapi.com"
DATA_DIR = "data"



def get_data(endpoint: str):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()



def create_data_folder():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)



def process_users(users_json):
    df_users = pd.json_normalize(users_json, sep="_")

    df_users = df_users.rename(columns={
        "id": "user_id",
        "name_firstname": "first_name",
        "name_lastname": "last_name",
        "address_city": "city",
        "address_geolocation_lat": "lat",
        "address_geolocation_long": "long"
    })

    df_users = df_users.fillna("Não informado")

    columns_to_keep = [
        "user_id",
        "first_name",
        "last_name",
        "email",
        "username",
        "city",
        "lat",
        "long"
    ]

    df_users = df_users[columns_to_keep]

    return df_users



def process_products(products_json):
    df_products = pd.json_normalize(products_json, sep="_")

    df_products = df_products.rename(columns={
        "id": "product_id",
        "title": "product_title",
        "price": "unit_price",
        "rating_rate": "rating",
        "rating_count": "rating_count"
    })

    df_products["unit_price"] = df_products["unit_price"].astype(float)
    df_products["rating"] = df_products["rating"].astype(float)
    df_products["rating_count"] = df_products["rating_count"].astype(int)

    df_products = df_products.fillna(0)

    columns_to_keep = [
        "product_id",
        "product_title",
        "category",
        "unit_price",
        "rating",
        "rating_count"
    ]

    df_products = df_products[columns_to_keep]

    return df_products



def process_transactions(carts_json, df_products):
    df_carts = pd.json_normalize(carts_json)

    df_carts["date"] = pd.to_datetime(df_carts["date"])

    df_transactions = df_carts.explode("products")

    df_transactions["product_id"] = df_transactions["products"].apply(lambda x: x["productId"])
    df_transactions["quantity"] = df_transactions["products"].apply(lambda x: x["quantity"])

    df_transactions = df_transactions.drop(columns=["products"])

    df_transactions = df_transactions.rename(columns={
        "userId": "user_id"
    })

    df_transactions["quantity"] = df_transactions["quantity"].astype(int)

    df_transactions = df_transactions.merge(
        df_products[["product_id", "unit_price"]],
        on="product_id",
        how="left"
    )

    df_transactions["total_value"] = (
        df_transactions["quantity"] * df_transactions["unit_price"]
    )

    columns_to_keep = [
        "date",
        "user_id",
        "product_id",
        "quantity",
        "unit_price",
        "total_value"
    ]

    df_transactions = df_transactions[columns_to_keep]

    return df_transactions



def create_date_dimension(df_transactions):
    min_date = df_transactions["date"].min()
    max_date = df_transactions["date"].max()

    df_date = pd.DataFrame({
        "date": pd.date_range(start=min_date, end=max_date)
    })

    df_date["year"] = df_date["date"].dt.year
    df_date["month"] = df_date["date"].dt.month
    df_date["month_name"] = df_date["date"].dt.month_name()
    df_date["quarter"] = df_date["date"].dt.quarter
    df_date["year_month"] = df_date["date"].dt.strftime("%Y-%m")

    return df_date



def main():
    print("Iniciando extração da Fake Store API...")

    create_data_folder()

    # Extração
    users_json = get_data("users")
    products_json = get_data("products")
    carts_json = get_data("carts")

    print("Dados extraídos com sucesso.")

    # Processamento
    df_users = process_users(users_json)
    df_products = process_products(products_json)
    df_transactions = process_transactions(carts_json, df_products)
    df_date = create_date_dimension(df_transactions)

    print("Dados processados com sucesso.")

    # Persistência
    df_users.to_csv(f"{DATA_DIR}/users.csv", index=False)
    df_products.to_csv(f"{DATA_DIR}/products.csv", index=False)
    df_transactions.to_csv(f"{DATA_DIR}/f_transactions.csv", index=False)
    df_date.to_csv(f"{DATA_DIR}/d_date.csv", index=False)

    print("Arquivos CSV gerados com sucesso na pasta /data.")
    print("Processo finalizado.")


if __name__ == "__main__":
    main()
