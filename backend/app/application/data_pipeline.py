import io
import re
import csv
from typing import Dict, Any, List, Tuple

# Try to import pandas, catch DLL/AppLocker load errors as well
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except (ImportError, Exception):
    PANDAS_AVAILABLE = False

class DataPipeline:
    # Basic Email Regex
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    # Basic Phone Regex (supports leading +, numbers, spaces, hyphens, min 7 digits, max 15 digits)
    PHONE_REGEX = re.compile(r"^\+?[0-9\s\-]{7,20}$")

    @classmethod
    def clean_name(cls, name: Any) -> str:
        if name is None or not isinstance(name, str):
            name = str(name) if name else ""
        # Remove multiple spaces, strip, and convert to Title Case
        clean = " ".join(name.split())
        return clean.title()

    @classmethod
    def clean_position(cls, position: Any) -> str:
        if position is None or not isinstance(position, str):
            position = str(position) if position else ""
        # Remove multiple spaces, strip, and convert to Title Case
        clean = " ".join(position.split())
        return clean.title()

    @classmethod
    def clean_email(cls, email: Any) -> str:
        if email is None or not isinstance(email, str):
            email = str(email) if email else ""
        # Strip and force strictly lowercase
        return email.strip().lower()

    @classmethod
    def clean_phone(cls, phone: Any) -> str:
        if phone is None:
            return ""
        phone = str(phone)
        # Strip spaces and characters, keep numbers, spaces, hyphens, and leading +
        clean = "".join(c for c in phone.strip() if c.isdigit() or c in ['+', '-', ' '])
        return clean

    @classmethod
    def _process_file_pandas(cls, file_content: bytes, file_name: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_content))
        else:
            df = pd.read_excel(io.BytesIO(file_content))

        # Rename columns to standard ones
        column_mapping = {}
        for col in df.columns:
            col_lower = str(col).lower().strip()
            if "name" in col_lower or "nombre" in col_lower:
                column_mapping[col] = "name"
            elif "email" in col_lower or "correo" in col_lower:
                column_mapping[col] = "email"
            elif "phone" in col_lower or "telefono" in col_lower or "teléfono" in col_lower:
                column_mapping[col] = "phone"
            elif "role" in col_lower or "position" in col_lower or "cargo" in col_lower or "puesto" in col_lower:
                column_mapping[col] = "position"

        df = df.rename(columns=column_mapping)

        for std_col in ["name", "email", "phone", "position"]:
            if std_col not in df.columns:
                df[std_col] = ""

        df = df[["name", "email", "phone", "position"]]

        valid_records = []
        discarded_records = []

        for idx, row in enumerate(df.itertuples(index=False), start=1):
            original_data = {
                "name": str(row.name) if not pd.isna(row.name) else "",
                "email": str(row.email) if not pd.isna(row.email) else "",
                "phone": str(row.phone) if not pd.isna(row.phone) else "",
                "position": str(row.position) if not pd.isna(row.position) else ""
            }

            c_name = cls.clean_name(row.name)
            c_email = cls.clean_email(row.email)
            c_phone = cls.clean_phone(row.phone)
            c_position = cls.clean_position(row.position)

            errors = cls._validate_record(c_name, c_email, c_phone)

            if errors:
                discarded_records.append({
                    "row_index": idx,
                    "original_data": original_data,
                    "reasons": errors
                })
            else:
                valid_records.append({
                    "name": c_name,
                    "email": c_email,
                    "phone": c_phone,
                    "position": c_position
                })

        return valid_records, discarded_records

    @classmethod
    def _process_file_pure_python(cls, file_content: bytes) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Pure Python fallback for CSV processing when Pandas C-extensions are blocked.
        """
        try:
            text = file_content.decode('utf-8')
        except UnicodeDecodeError:
            text = file_content.decode('latin-1', errors='ignore')

        reader = csv.reader(io.StringIO(text))
        try:
            header = next(reader)
        except StopIteration:
            return [], []

        # Find column mappings
        name_idx, email_idx, phone_idx, pos_idx = -1, -1, -1, -1
        for idx, col in enumerate(header):
            col_lower = col.lower().strip()
            if "name" in col_lower or "nombre" in col_lower:
                name_idx = idx
            elif "email" in col_lower or "correo" in col_lower:
                email_idx = idx
            elif "phone" in col_lower or "telefono" in col_lower or "teléfono" in col_lower:
                phone_idx = idx
            elif "role" in col_lower or "position" in col_lower or "cargo" in col_lower or "puesto" in col_lower:
                pos_idx = idx

        valid_records = []
        discarded_records = []

        for idx, row in enumerate(reader, start=1):
            if not row or all(not cell.strip() for cell in row):
                continue  # skip empty lines

            # Extract fields safely
            name_val = row[name_idx] if 0 <= name_idx < len(row) else ""
            email_val = row[email_idx] if 0 <= email_idx < len(row) else ""
            phone_val = row[phone_idx] if 0 <= phone_idx < len(row) else ""
            pos_val = row[pos_idx] if 0 <= pos_idx < len(row) else ""

            original_data = {
                "name": name_val,
                "email": email_val,
                "phone": phone_val,
                "position": pos_val
            }

            c_name = cls.clean_name(name_val)
            c_email = cls.clean_email(email_val)
            c_phone = cls.clean_phone(phone_val)
            c_position = cls.clean_position(pos_val)

            errors = cls._validate_record(c_name, c_email, c_phone)

            if errors:
                discarded_records.append({
                    "row_index": idx,
                    "original_data": original_data,
                    "reasons": errors
                })
            else:
                valid_records.append({
                    "name": c_name,
                    "email": c_email,
                    "phone": c_phone,
                    "position": c_position
                })

        return valid_records, discarded_records

    @classmethod
    def _validate_record(cls, name: str, email: str, phone: str) -> List[str]:
        errors = []
        if not name:
            errors.append("El nombre no puede estar vacío.")
        
        if not email:
            errors.append("El correo electrónico no puede estar vacío.")
        elif not cls.EMAIL_REGEX.match(email):
            errors.append(f"El correo '{email}' no tiene un formato válido.")
            
        if phone and not cls.PHONE_REGEX.match(phone):
            errors.append(f"El teléfono '{phone}' no tiene un formato válido.")
            
        return errors

    @classmethod
    def process_file(cls, file_content: bytes, file_name: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Processes file using Pandas if available, or falls back to pure Python for CSV.
        """
        if PANDAS_AVAILABLE:
            return cls._process_file_pandas(file_content, file_name)
        else:
            if not file_name.endswith('.csv'):
                raise ValueError(
                    "Pandas no está disponible debido a restricciones del sistema (AppLocker/C-extensions). "
                    "Por favor suba el archivo únicamente en formato CSV."
                )
            return cls._process_file_pure_python(file_content)
