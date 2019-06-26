'''
            {
              "name": "APPLE",
              "label": "APPLE",
              "type": "timeseries",
              "color": "#2196f3",
              "settings": {},
              "_hash": 0.09058572711104071
            },
'''

startText = '''{
  "widget": {
    "isSystemType": true,
    "bundleAlias": "charts",
    "typeAlias": "bars",
    "type": "latest",
    "title": "Bars - Chart.js",
    "sizeX": 18,
    "sizeY": 9,
    "row": 0,
    "col": 3,
    "config": {
      "datasources": [
        {
          "type": "entity",
          "entityAliasId": "8d34a557-ebd9-bd8c-49a8-1a9f58132e62",
          "dataKeys": [
'''
endText = '''
          ]
        }
      ],
      "timewindow": {
        "realtime": {
          "timewindowMs": 60000
        }
      },
      "showTitle": true,
      "backgroundColor": "#fff",
      "color": "rgba(0, 0, 0, 0.87)",
      "padding": "8px",
      "settings": {},
      "title": "Bars - Chart.js",
      "dropShadow": true,
      "enableFullscreen": true,
      "widgetStyle": {},
      "titleStyle": {
        "fontSize": "16px",
        "fontWeight": 400
      },
      "useDashboardTimewindow": true,
      "showLegend": false,
      "actions": {}
    },
    "id": "ecb10f0f-cf0f-d75f-118b-aa7b7de7799f"
  },
  "aliasesInfo": {
    "datasourceAliases": {
      "0": {
        "alias": "grafico_marca",
        "filter": {
          "type": "singleEntity",
          "singleEntity": {
            "entityType": "DEVICE",
            "id": "6dbcf0d0-9769-11e9-a964-c51b3a6f7239"
          },
          "resolveMultiple": false
        }
      }
    },
    "targetDeviceAliases": {}
  },
  "originalSize": {
    "sizeX": 18,
    "sizeY": 9
  },
  "originalColumns": 24
}'''

from random import random
from random import randint

def geraCor():
    cor = '#'
    for x in range(3):
        cor += str(hex(randint(0,255))[2:])
    
    return cor
def generate_chart_keys_list(lKeys):
    global startText
    global endText
    text = ''
    #tabs = "\t\t\t"
    tabs = " "*12
    space = "  "
    tabspc = tabs + space
    jumpLineStart = '\n'
    jumpLine = ',' + jumpLineStart

    for key in lKeys:
        text += tabs + "{" + jumpLineStart
        text += tabspc + '"name": "%s"'%(key) + jumpLine
        text += tabspc + '"label": "%s"'%(key) + jumpLine
        text += tabspc + '"type": "timeseries"' + jumpLine
        text += tabspc + '"color": "%s"'%(geraCor()) + jumpLine
        text += tabspc + '"settings": {}' + jumpLine
        text += tabspc + '"_hash": %.17f'%(random()) + jumpLineStart
        text += tabs + "}" + jumpLine

    return (startText + text[:-2] + endText)

def save_output(lista, filename='output.json'):
    output = generate_chart_keys_list(lista)

    arq = open(filename, 'w')
    arq.write(output)
    arq.close()

if(__name__ == "__main__"):
    lista = ['APPLE', "SAMSUNG", "NOKIA"]
    save_output(range(1,10001))