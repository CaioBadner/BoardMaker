import boto3
import json

# Create a DynamoDB client
#dynamodb = boto3.client('dynamodb', region_name = 'us-east-1')

# JSON data to be stored
json_data =     {
        "language": "PT",
        "rows": 4,
        "columns": 4,
        "totalWords": 47,
        "tiles": [
            "E",
            "X",
            "E",
            "N",
            "I",
            "A",
            "I",
            "O",
            "H",
            "C",
            "B",
            "F",
            "I",
            "T",
            "O",
            "O"
        ],
        "wordCount": [
            0,
            0,
            0,
            0,
            25,
            10,
            7,
            0,
            2,
            1,
            2,
            0,
            0,
            0,
            0,
            0
        ],
        "normalGuesses": {
            "ABONE": "0510070302",
            "ABONEI": "051007030206",
            "ACIONE": "050906070302",
            "BACO": "10050914",
            "BAIXE": "1005040100",
            "BAIXEI": "100504010206",
            "BICA": "10060905",
            "BICO": "10060914",
            "BOCA": "10140905",
            "BOCHA": "1014090805",
            "BOCIO": "1014090607",
            "BOIA": "10070605",
            "BOIE": "10070602",
            "BONE": "10070302",
            "CABINE": "090510060302",
            "CABO": "09051007",
            "CAIBO": "0905061007",
            "CAIE": "09050400",
            "CAIO": "09050607",
            "CHIA": "09080405",
            "CHIE": "09080400",
            "CINE": "09060302",
            "CITO": "09121314",
            "FICA": "11060905",
            "FICHA": "1106090805",
            "FICO": "11060914",
            "FINO": "11060307",
            "FIXA": "11060105",
            "FIXE": "11060100",
            "FIXEI": "1106010004",
            "FOBIA": "1107100605",
            "FOBICO": "110710060914",
            "FOCA": "11140905",
            "FONE": "11070302",
            "FONICA": "110703060905",
            "FONICO": "110703060914",
            "OBOE": "14100702",
            "OCIO": "14090607",
            "ONIX": "07030601",
            "OTICA": "1413120905",
            "TOCA": "13140905",
            "TOCHA": "1314090805",
            "XENOFOBA": "0102030711141005",
            "XENOFOBIA": "010203071114100605",
            "XENOFOBICA": "01020307111410060905",
            "XENOFOBICO": "01020307111510060914",
            "XENOFOBO": "0102030711141015"
        },
        "tilesStarting": [
            0,
            5,
            0,
            0,
            0,
            3,
            0,
            1,
            0,
            9,
            11,
            13,
            0,
            2,
            3,
            0
        ],
        "tilesUsed": [
            5,
            11,
            15,
            16,
            6,
            28,
            28,
            24,
            5,
            29,
            24,
            18,
            2,
            4,
            20,
            2
        ],
        "bonusGuesses": {
            "ABICO": "0510060914",
            "ABIO": "05100607",
            "ACIO": "05090607",
            "ACTO": "05091314",
            "AEON": "05020703",
            "AINO": "05060307",
            "AXION": "0501060703",
            "BACIO": "1005090607",
            "BAHT": "10050813",
            "BAIXIO": "100504010607",
            "BICAI": "1006090504",
            "BICHA": "1006090805",
            "BICHAI": "100609080504",
            "BICI": "10060904",
            "BOFIA": "1007110605",
            "BOIAI": "1007060504",
            "BOICA": "1007060905",
            "BOOT": "10151413",
            "BOTCHA": "101413090805",
            "BOTICA": "101413120905",
            "CHIAI": "0908040506",
            "CIBO": "09061007",
            "COBI": "09141006",
            "COBO": "09141007",
            "COBOI": "0914100706",
            "COFIA": "0914110605",
            "COFIAI": "091411060504",
            "COFIE": "0914110602",
            "COFIO": "0914110607",
            "COFO": "09141107",
            "ENOFOBIA": "0203071114100605",
            "EONICO": "020703060914",
            "EXACTO": "000105091314",
            "EXIBA": "0001061005",
            "EXIBO": "0001061007",
            "FIAI": "11060504",
            "FICAI": "1106090504",
            "FICHAI": "110609080504",
            "FINE": "11060302",
            "FIXAI": "1106010504",
            "FOCAI": "1114090504",
            "FONIX": "1107030601",
            "HAXE": "08050100",
            "HITO": "08121314",
            "ICAI": "04090506",
            "INEXACTO": "0603020105091314",
            "NEOFOBA": "03020711141005",
            "NEOFOBIA": "0302071114100605",
            "NEOFOBICA": "030207111410060905",
            "NEOFOBICO": "030207111510060914",
            "NEOFOBO": "03020711141015",
            "NICA": "03060905",
            "NOIA": "03070605",
            "OFICIA": "071106090405",
            "OFICIE": "071106090400",
            "OIAI": "07060504",
            "OICA": "07060905",
            "OICO": "07060914",
            "THIA": "13080405",
            "TICA": "13120905",
            "TICAI": "1312090504",
            "TICO": "13120914",
            "TOBA": "13141005",
            "TOCAI": "1314090504",
            "TOCAIE": "131409050400",
            "TOCAIO": "131409050607",
            "TOCHAI": "131409080504",
            "TOFO": "13141107",
            "XEICA": "0100040905",
            "XENIO": "0102030607"
        }
    }

# Serialize JSON data to a string
json_data_str = json.dumps(json_data)

# Prepare the DynamoDB item
dynamodb_item = {
    "Id": {
        "S": "daily20240604"
    },
    "Data": {
        "S": json_data_str
    }
}

# Serialize the DynamoDB item to a JSON string for manual insertion
dynamodb_item_str = json.dumps(dynamodb_item, indent=4)
print(dynamodb_item_str)


# Insert item into DynamoDB
# NEED TO FIX CREDENTIALS
"""
dynamodb.put_item(
    TableName='DuelangoBoard',
    Item={
        'id': {'S': 'daily20240602'},
        'data': {'S': json_data_str}
    }
)"""