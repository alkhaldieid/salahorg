#! /home/alkhaldieid/anaconda3/bin/python
import datetime
import requests
import pandas 
import calendar


def get_current_month():
    today = datetime.date.today()
    return today.month, today.year



def load_times_file(loc_path, prayers):
    df = pandas.read_csv(loc_path)
    strdates = [df['Date'][x] for x in range(df['Date'].size)]
    strdf = [[0 for x in range(df[prayers[0]].size)] for y in range(len(prayers))] #initialize the str list with zeros

    for i in range(len(prayers)):
        df[prayers[i]] = pandas.to_datetime(df[prayers[i]] , infer_datetime_format=True, errors='coerce').dt.time
        for j in range(df[prayers[i]].size):
            strdf[i][j] = df[prayers[i]][j].strftime('%H:%M')
            if i > 2:
                strdf[i][j] = str(int(strdf[i][j][:2]) + 12) +strdf[i][j][2:]
    return df, strdf, strdates

class SalahOrg(object):
    def __init__(self):
        self.month, self.year = get_current_month()
        self.path = '/home/alkhaldieid/repos/salahorg/data/{}_{}.csv'.format(self.year,self.month)
        self.output_path = '/home/alkhaldieid/repos/salahorg/data/{}_{}.org'.format(self.year,self.month)
        self.prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]
        self.df, self.strdf, self.strdates = load_times_file(self.path, prayers = self.prayers)
        self.month_range = calendar.monthrange(self.year, self.month)
        self.url = self.get_url


    def get_url(self):
        return "https://www.salahtimes.com/usa/toledo/csv?highlatitudemethod=4&prayercalculationmethod=5&asarcalculationmethod=1&displayas24hour=false&start={}-{}-01&end={}-{}-{}".format(self.year, self.month, self.year, self.month, self.month_range[1])

    def get_month_page(self):
        page = requests.get(self.url())
        with open(self.path, 'wb') as f:
            f.write(page.content)


    def make_org_file(self):
        print('#+STARTUP: overview')
        for i, date in enumerate(self.strdates):
            print("* {}".format(date))
            for prayer in self.prayers:
                if prayer == "Sunrise":
                    pass
                else:
                    print("** TODO {}".format(prayer))
                    if i > 8:
                        if prayer == "Fajr":
                            print("  SCHEDULED: <{}-{}-{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[0][i],self.strdf[1][i]))
                        elif prayer == 'Dhuhr':
                            print("  SCHEDULED: <{}-{}-{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[2][i],self.strdf[3][i]))
                        elif prayer == 'Asr':
                            print("  SCHEDULED: <{}-{}-{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[3][i],self.strdf[4][i]))
                        elif prayer == 'Maghrib':
                            print("  SCHEDULED: <{}-{}-{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[4][i],self.strdf[5][i]))
                        else:
                            print("  SCHEDULED: <{}-{}-{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[5][i],"23:59"))
                    else:
                        if prayer == "Fajr":
                            print("  SCHEDULED: <{}-{}-0{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[0][i],self.strdf[1][i]))
                        elif prayer == 'Dhuhr':
                            print("  SCHEDULED: <{}-{}-0{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[2][i],self.strdf[3][i]))
                        elif prayer == 'Asr':
                            print("  SCHEDULED: <{}-{}-0{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[3][i],self.strdf[4][i]))
                        elif prayer == 'Maghrib':
                            print("  SCHEDULED: <{}-{}-0{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[4][i],self.strdf[5][i]))
                        else:
                            print("  SCHEDULED: <{}-{}-0{} {} {}-{}>".format(self.year,self.month,self.strdates[i][4:6],self.strdates[i][:3],self.strdf[5][i],"23:59"))


if __name__=="__main__":
    salah = SalahOrg()
    # salah.make_org_file("ou")
    # print(salah.month_range[1])
    # print(salah.get_url())
    salah.get_month_page()
    salah.make_org_file()
