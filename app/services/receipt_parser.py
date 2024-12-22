from datetime import datetime
import re
from app.models.receipt import Receipt, ReceiptItem

class ReceiptParser:
    @staticmethod
    def parse_text(text: str) -> Receipt:
        """
        Parse the OCR text into structured receipt data
        """
        # Initialize default values
        merchant_name = ""
        date = datetime.now()
        total_amount = 0.0
        items = []
        
        lines = text.split('\n')
        
        # Basic parsing logic (you'll need to enhance this based on your receipts)
        for i, line in enumerate(lines):
            # Try to find merchant name (usually in first few lines)
            if i < 3 and not merchant_name and len(line.strip()) > 0:
                merchant_name = line.strip()
            
            # Look for date
            date_match = re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', line)
            if date_match:
                try:
                    date = datetime.strptime(date_match.group(), '%m/%d/%Y')
                except:
                    pass
            
            # Look for total amount
            total_match = re.search(r'total[\s:]*[$]?\s*(\d+\.\d{2})', line.lower())
            if total_match:
                total_amount = float(total_match.group(1))
            
            # Try to find items (this is a basic example)
            item_match = re.search(r'(.*?)\s+(\d+\.\d{2})', line)
            if item_match and '$' in line:
                name = item_match.group(1).strip()
                price = float(item_match.group(2))
                items.append(ReceiptItem(
                    name=name,
                    quantity=1.0,  # Default quantity
                    price=price,
                    total=price
                ))
        
        return Receipt(
            merchant_name=merchant_name,
            date=date,
            total_amount=total_amount,
            items=items
        )
