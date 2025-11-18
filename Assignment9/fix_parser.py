class FixParser:
    def __init__(self, delimiter='|'): 
        self.delimiter = delimiter

    def parse(self, message):
        fields = message.split(self.delimiter)
        fix_dict = {}
        for field in fields:
            if '=' in field:
                tag, value = field.split('=', 1)
                fix_dict[tag] = value
        print(fix_dict)

        if '44' not in fix_dict  or '54' not in fix_dict: #price and side
            raise ValueError("Missing required fields: 'price' and 'side'")
            
        return fix_dict

if __name__ == "__main__":
    # msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128"
    msg = "8=FIX.4.2|35=D|55=AAPL|44=50|54=1|38=100|40=2|10=128" #added 44 Price
    print(FixParser().parse(msg))