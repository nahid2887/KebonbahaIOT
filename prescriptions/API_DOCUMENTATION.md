# Prescription API Documentation

## Example Request Bodies

### Submit Prescription API

**Endpoint:** `POST /api/submit-prescription/`

**Request Body Example:**
```json
{
  "rx_number": "RX123456789",
  "store_number": "1234",
  "pharmacy_or_doctor_name": "CVS Pharmacy",
  "contact_details": "(555) 123-4567",
  "date_filled": "07/20/2025",
  "date_expired": "07/20/2026",
  "address": "123 Main St, City, State 12345",
  "medicines_names": [
    {
      "medicine_name": "Lisinopril",
      "generic_name": "Lisinopril",
      "instructions": "Take 1 tablet by mouth daily",
      "qty": "30",
      "refills_info": "5 refills remaining",
      "side_effects": "Dizziness, dry cough"
    },
    {
      "medicine_name": "Metformin",
      "generic_name": "Metformin HCl",
      "instructions": "Take 1 tablet twice daily with meals",
      "qty": "60",
      "refills_info": "3 refills remaining",
      "side_effects": "Nausea, stomach upset"
    }
  ]
}
```

### OCR Prescription Extraction API

**Endpoint:** `POST /api/extract-prescription-ocr/`

**Request:** Multipart form data with image file(s)
- Key: `image`
- Value: Image file (JPG, PNG, etc.)

**Response Example:**
```json
{
  "rx_number": "RX123456789",
  "store_number": "1234",
  "pharmacy_or_doctor_name": "CVS Pharmacy",
  "contact_details": "(555) 123-4567",
  "date_filled": "07/20/2025",
  "date_expired": "07/20/2026",
  "address": "123 Main St, City, State 12345",
  "medicines_names": [
    {
      "medicine_name": "Lisinopril",
      "generic_name": "Lisinopril",
      "instructions": "Take 1 tablet by mouth daily",
      "qty": "30",
      "refills_info": "5 refills remaining",
      "side_effects": "Dizziness, dry cough"
    }
  ]
}
```

### Get User Prescriptions API

**Endpoint:** `GET /api/user-prescriptions/`

**Response Example:**
```json
[
  {
    "id": 1,
    "rx_number": "RX123456789",
    "department_number": "1234",
    "dob": "2000-01-01",
    "pharmacy_or_doctor_name": "CVS Pharmacy",
    "contact_details": "(555) 123-4567",
    "date_filled": "07/20/2025",
    "date_expired": "07/20/2026",
    "address": "123 Main St, City, State 12345",
    "store_number": "1234",
    "rx_image": null,
    "created_at": "2025-07-20T10:30:00Z",
    "medicines": [
      {
        "id": 1,
        "medicine_name": "Lisinopril",
        "generic_name": "Lisinopril",
        "instructions": "Take 1 tablet by mouth daily",
        "qty": "30",
        "refills_info": "5 refills remaining",
        "side_effects": "Dizziness, dry cough",
        "prescription": 1
      }
    ]
  }
]
```

## Authentication

All prescription endpoints require authentication. Include the Bearer token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Accessing Swagger Documentation

Once the server is running, you can access the interactive API documentation at:
- **Swagger UI:** `http://localhost:8000/swagger/`
- **ReDoc:** `http://localhost:8000/redoc/` (if configured)
- **JSON Schema:** `http://localhost:8000/swagger.json`

## Testing the APIs

1. First, authenticate via the auth endpoints to get a JWT token
2. Use the token in the Authorization header for prescription endpoints
3. Test OCR by uploading prescription images
4. Submit prescription data manually or from OCR results
5. Retrieve user prescriptions to verify data was saved correctly
