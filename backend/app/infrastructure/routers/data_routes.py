from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any, List
from app.application.data_pipeline import DataPipeline

router = APIRouter(
    prefix="/data",
    tags=["data-normalization"]
)

@router.post("/normalize-contacts", response_model=Dict[str, Any])
async def normalize_contacts(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Sube una lista de contactos en CSV o Excel y realiza un proceso de normalización
    estricta utilizando Pandas (Capitalización Title Case en nombres, emails minúsculas absolutas,
    validaciones de teléfonos e índices de error).
    """
    if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
        raise HTTPException(
            status_code=400,
            detail="Formato de archivo no válido. Debe subir un archivo CSV o Excel (.xlsx, .xls)."
        )

    try:
        content = await file.read()
        valid_records, discarded_records = DataPipeline.process_file(content, file.filename)
        
        return {
            "success": True,
            "filename": file.filename,
            "summary": {
                "total_processed": len(valid_records) + len(discarded_records),
                "valid_records_count": len(valid_records),
                "discarded_records_count": len(discarded_records)
            },
            "valid_records": valid_records,
            "discarded_records": discarded_records
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )
