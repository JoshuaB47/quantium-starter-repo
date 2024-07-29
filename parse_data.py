import csv
class DataParser:
    def __init__(self):
        self.rows = []
    def processDataSheet(self, sheetName):
        with open(sheetName, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # only include pink morsels
                if row["product"] == "pink morsel":
                    self.rows.append({"sales" : self.getSales(row),
                                    "date" : row["date"],
                                    "region" : row["region"]})

    def getSales(self, row):
        # quantity times price (rounded to two decimal places and removing the dollar sign)
        return int(row["quantity"]) * round((float(row["price"][1:])), 2)

    def writeData(self):
        with open('munged.csv', 'w', newline='') as csvfile:
            # there's three fields that we want
            fieldnames = ['sales', 'date', 'region']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # write the top row of csv
            writer.writeheader()
            # write all the rows
            for row in self.rows:
                writer.writerow(row)

    def dealWithAllSheets(self):
        for sheetName in ["data/daily_sales_data_0.csv",
                          "data/daily_sales_data_1.csv",
                          "data/daily_sales_data_2.csv"]:
            self.processDataSheet(sheetName)
        self.writeData()
if __name__ == "__main__":
    DataParser().dealWithAllSheets()