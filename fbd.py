from processing_request import app

if __name__ == '__main__':
    app.run(debug=True)
    # BD = DataBase()
    # rows = BD.get_last_time_from_last_online_time("2355_10")
    # print(rows[0][1].strftime("%d-%b-%Y %H:%M:%S.%f"))
