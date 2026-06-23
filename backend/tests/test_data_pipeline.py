from app.application.data_pipeline import DataPipeline

def test_data_pipeline_normalization():
    # Mock CSV data
    csv_data = (
        "Nombre,Correo,Telefono,Cargo\n"
        "gustavo navarro,Gustavo@EMPRESA.COM,+57 315-123-4567,INGENIERO DE SOFTWARE\n"
        "LAURA RIOS,laura.rios@email.com,invalid-phone-abc,AUXILIAR CONTABLE\n"
        " ,invalid-email,3001234567,Diseñador\n"
    )
    
    csv_bytes = csv_data.encode('utf-8')
    valid, discarded = DataPipeline.process_file(csv_bytes, "test_contacts.csv")
    
    # Assertions for Valid Records
    assert len(valid) == 1
    first_record = valid[0]
    assert first_record["name"] == "Gustavo Navarro"          # Title Case
    assert first_record["email"] == "gustavo@empresa.com"     # Lowercase
    assert first_record["phone"] == "+57 315-123-4567"        # Kept phone format
    assert first_record["position"] == "Ingeniero De Software"# Title Case
    
    # Assertions for Discarded Records
    assert len(discarded) == 2
    
    # Row 2 discarded due to phone
    row_2_discarded = [r for r in discarded if r["row_index"] == 2][0]
    assert any("teléfono" in reason.lower() for reason in row_2_discarded["reasons"])
    
    # Row 3 discarded due to missing name and invalid email
    row_3_discarded = [r for r in discarded if r["row_index"] == 3][0]
    assert any("nombre" in reason.lower() for reason in row_3_discarded["reasons"])
    assert any("correo" in reason.lower() for reason in row_3_discarded["reasons"])

if __name__ == "__main__":
    test_data_pipeline_normalization()
    print("test_data_pipeline_normalization PASSED successfully!")
