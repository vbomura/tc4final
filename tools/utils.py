from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler,LabelEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
import pandas as pd


#Alterando nomes das colunas
class RenomearColunasTransf(BaseEstimator, TransformerMixin):
    def __init__(self, columns_map=None):
        columns_map = {'Gender':'genero',
                'Age':'idade',
                'Height':'altura',
                'Weight':'peso',
                'family_history':'historico_familiar',
                'FAVC':'calorias_frequente',
                'FCVC':'vegetais_refeicao',
                'NCP':'refeicoes_diaria',
                'CAEC':'entre_refeicao',
                'SMOKE':'fuma',
                'CH2O':'litros_agua',
                'SCC':'monitora_calorias',
                'FAF':'frequencia_atividade',
                'TUE':'tempo_tecnologia',
                'CALC':'frequencia_alcool',
                'MTRANS':'transporte_usado',
                'Obesity':'nvl_obsidade'}
        self.columns_map = columns_map if columns_map is not None else {}

    def fit(self, X, y=None):
        # Nada a aprender, apenas retorna o próprio objeto
        return self

    def transform(self, X):
        X_ = X.copy()
        X_.rename(columns=self.columns_map, inplace=True)
        return X_
    
class MultiLabelEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        """
        columns: lista de colunas a codificar com LabelEncoder
        """
        self.columns = columns
        self.encoders = {}

    def fit(self, X, y=None):
        X_ = X.copy()
        for col in self.columns:
            le = LabelEncoder()
            le.fit(X_[col])
            self.encoders[col] = le
        return self

    def transform(self, X):
        X_ = X.copy()
        for col, le in self.encoders.items():
            X_[f"{col}_cod"] = le.transform(X_[col])
        return X_
    
class YesNoToBinaryTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        columns = ['historico_familiar', 'calorias_frequente', 'fuma', 'monitora_calorias']
        self.columns = columns

    def fit(self, X, y=None):
        # Nada a aprender, apenas retorna o próprio transformer
        return self

    def transform(self, X):
        X_ = X.copy()

        mapping = {'yes': 1, 'no': 0}

        # Converte apenas as colunas selecionadas
        for col in self.columns:
            if col in X_.columns:
                X_[col] = X_[col].map(mapping)

        return X_
    
"""     def __init__(self,min_max_scaler=['idade','altura','peso','vegetais_refeicao','refeicoes_diaria','litros_agua','frequencia_atividade']): """    
class MinMax(BaseEstimator, TransformerMixin):
    def __init__(self,min_max_scaler=['vegetais_refeicao','refeicoes_diaria','litros_agua','frequencia_atividade']):
        self.min_max_scaler = min_max_scaler

    def fit(self, df):
        return self
    
    def transform(self, df):
        if(set(self.min_max_scaler).issubset(df.columns)):
            min_max_enc = MinMaxScaler()
            df[self.min_max_scaler] = min_max_enc.fit_transform(df[self.min_max_scaler])
            return df
        else:
            print('Uma ou mais colunas não existentes, por favor verifique!')
            return df
        
class OrdinalEncodingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, encoding_map=None):
        encoding_map = {
            "entre_refeicao": ["no", "Sometimes", "Frequently", "Always"],
            "frequencia_alcool": ["no", "Sometimes", "Frequently", "Always"],
            "nvl_obsidade": [
                "Insufficient_Weight",
                "Normal_Weight",
                "Overweight_Level_I",
                "Overweight_Level_II",
                "Obesity_Type_I",
                "Obesity_Type_II",
                "Obesity_Type_III"
            ]
        }
        self.encoding_map = encoding_map
        self.encoders = {}

    def fit(self, X, y=None):
        X_ = X.copy()

        for col, ordem in self.encoding_map.items():
            enc = OrdinalEncoder(
                categories=[ordem],
                handle_unknown='use_encoded_value',
                unknown_value=-1
            )
            enc.fit(X_[[col]])
            self.encoders[col] = enc

        return self

    def transform(self, X):
        X_ = X.copy()

        for col, enc in self.encoders.items():
            X_[f"{col}_ord"] = enc.transform(X_[[col]])

        return X_
    
class DummyEncoderTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None, prefix=None, drop_first=False):
        columns=["transporte_usado"]
        prefix="transporte"
        self.columns = columns
        self.prefix = prefix
        self.drop_first = drop_first
        self.dummy_columns = None  # será definido no fit

    def fit(self, X, y=None):
        X_ = X.copy()
        dummies = pd.get_dummies(
            X_,
            columns=self.columns,
            prefix=self.prefix,
            drop_first=self.drop_first
        )
        self.dummy_columns = dummies.columns  # guardamos as colunas finais do fit
        return self

    def transform(self, X):
        X_ = X.copy()
        dummies = pd.get_dummies(
            X_,
            columns=self.columns,
            prefix=self.prefix,
            drop_first=self.drop_first
        )

        # Garante que tenham as mesmas colunas do fit()
        for col in self.dummy_columns:
            if col not in dummies:
                dummies[col] = 0

        # Remove colunas extras que não existiam no fit
        dummies = dummies[self.dummy_columns]

        return dummies
    
class ColumnsToIntTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):
        columns = [
            "transporte_Automobile",
            "transporte_Bike",
            "transporte_Motorbike",
            "transporte_Public_Transportation",
            "transporte_Walking"
        ]        
        self.columns = columns

    def fit(self, X, y=None):
        return self  # Nada para ajustar

    def transform(self, X):
        X_ = X.copy()
        for col in self.columns:
            if col in X_.columns:
                X_[col] = X_[col].astype(int)
        return X_