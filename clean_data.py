"""Taller evaluable presencial"""

import pandas as pd


def load_data(input_file):
    """Lea el archivo usando pandas y devuelva un DataFrame"""
    data = pd.read_csv(input_file, sep="\t")
    return data


def create_key(df, n):
    """Cree una nueva columna en el DataFrame que contenga el key de la columna 'text'"""

    df = df.copy()

    df["fingerprint"] = (
        df["fingerprint"]
    # 2. Remueva los espacios en blanco al principio y al final de la cadena
        .str.strip()
    # 3. Convierta el texto a minúsculas
        .str.lower()
    # 4. Transforme palabras que pueden (o no) contener guiones por su version sin guion.
        .str.replace("-", "")
    # 5. Remueva puntuación y caracteres de control
        .str.translate(
           str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
        )
    
    # 6. Convierta el texto a una lista de tokens
        .str.split()
    # Una el texto sin espacios en blanco
        .sty.join("")
    # Convierta el texto a una lista de n-gramas
        .apply(lambda x: [x[i:i + n] for i in range(len(x) - n + 1)])
    # Ordene la lista de n-gramas y remueve duplicados
        .apply(lambda x: sorted(set(x)))
    )
    # Una el texto sin espacios en blanco
    
    
    # Convierta la lista de ngramas a una cadena
    
    return df


def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame"""

    df = df.copy()

    # 1. Ordene el dataframe por 'fingerprint' y 'text'
    df = df.sort_values(by=["fingerprint", "text"]).copy()
    # 2. Seleccione la primera fila de cada grupo de 'fingerprint'
    fingerprints = df.groupby("fingerprint").first().reset_index()
    # 3.  Cree un diccionario con 'fingerprint' como clave y 'text' como valor
    fingerprints = fingerprints.set_index("fingerprint")["text"].to_dict()
    # 4. Cree la columna 'cleaned' usando el diccionario
    df["cleaned"] = df["fingerprint"].map(fingerprints)

    return df


def save_data(df, output_file):
    """Guarda el DataFrame en un archivo"""

    df = df.copy()
    df = df[["cleaned"]]
    df = df.rename(columns={"cleaned": "text"})
    df.to_csv(output_file, sep="\t", index=False)



def main(input_file, output_file, n=2):
    """Ejecuta la limpieza de datos"""

    df = load_data(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv("test.csv", index=False)
    save_data(df, output_file)


if __name__ == "__main__":
    main(
        input_file="input.txt",
        output_file="output.txt",
    )
