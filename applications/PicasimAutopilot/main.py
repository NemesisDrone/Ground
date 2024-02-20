from picasim import PicaSimConnector


if __name__ == "__main__":
    pica_sim = PicaSimConnector()
    while True:
        data_input = input("Enter data to send: ")

        if data_input == "exit":
            break
        pica_sim.send_data(data_input)

    pica_sim.close()
