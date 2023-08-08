import pyshark
import keyboard
from User import *

count_packets = 0
bo = False


class NetworkAnalyzer():
    def __init__(self, entrada):
        self.capture = None
        self.ip = None
        self.count_sem_ip = 0
        self.entrada = int(entrada)
        self.count_anom = 0


    global count_packets

    def start_packet_capture(self):
        global count_packets
        self.tamanho_total = 0
        self.capture = pyshark.LiveCapture()
        for raw_packet in self.capture.sniff_continuously():
            count_packets += 1
            packet_size = self.calculate_packet_size(raw_packet)
            self.tamanho_total += packet_size
            print(self.filter_packets(raw_packet, self.entrada))
            print(f"Packet {count_packets} - Size: {packet_size} bytes \n")

            if keyboard.is_pressed('esc'):
                self.stop_packet_capture()

    def stop_packet_capture(self):
        self.capture.close()

    def get_packet_count(self):
        return count_packets
    def identify_anomalies(self):
        return self.count_anom

    def filter_packets(self, packet, entrada):
        # Verifica se a camada 'IP' está presente
        if 'IP' in packet:
            self.source_address = packet['IP'].src
            self.destination_address = packet['IP'].dst

            # Verifica se o atributo 'length' está presente na camada IP
            if hasattr(packet['IP'], 'length'):
                self.length = int(packet['IP'].length)
            else:
                self.count_anom += 1
                self.length = 'N/A'
        else:
            self.count_anom += 1
            self.length = 'N/A'
            self.source_address = 'N/A'
            self.destination_address = 'N/A'

        # Verifica se a camada 'tcp' ou 'udp' está presente e obtém as portas
        if 'TCP' in packet and 'tcp' in packet:
            self.protocol = 'TCP'
            self.source_port = packet['TCP'].srcport
            self.destination_port = packet['TCP'].dstport
        elif 'UDP' in packet and 'udp' in packet:
            self.protocol = 'UDP'
            self.source_port = packet['UDP'].srcport
            self.destination_port = packet['UDP'].dstport
        else:
            self.count_anom +=1
            self.protocol = 'N/A'
            self.source_port = 'N/A'
            self.destination_port = 'N/A'
            self.count_sem_ip += 1

        self.packet_time = packet.sniff_time
        if entrada == 1:
            return f'\nSource address: {self.source_address}' \
                   f'\nSource port: {self.source_port}'
        if entrada == 2:
            return f'\nDestination address: {self.destination_address}' \
                   f'\nDestination port: {self.destination_port}'
        if entrada == 3:
            return f'Packet Timestamp: {self.packet_time}' \
                   f'\nProtocol type: {self.protocol}' \
                   f'\nSource address: {self.source_address}' \
                   f'\nSource port: {self.source_port}' \
                   f'\nDestination address: {self.destination_address}' \
                   f'\nDestination port: {self.destination_port}'


    def calculate_packet_size(self, packet):
        # Convertendo o pacote para uma string
        packet_str = str(packet)

        # Calculando o tamanho do pacote em bytes
        packet_size = len(packet_str)

        return packet_size

    def get_bandwidth(self, packet, tamanho):
        tempo_decorrido = packet[-1].sniff_time - packet[0].sniff_time
    # Resto do código não foi alterado...


usuario = User()

while usuario.login() == False:
    print('Tente novamente')

opcao = int(input("Escolha uma opção: \n 1 - Filtrar apenas informações da origem;\n "
          "2 - Filtrar apenas informações do destino;"
          "\n 3 - Filtrar informações de origem e destino \n 4 - Encerrar programa \n"))
if opcao == 4:
    print('Obrigado pelo acesso!')
else:
    analisador = NetworkAnalyzer(opcao)
    analisador.start_packet_capture()
    # p.gerar_relatorio_trafego_rede()
    print(f'Quantidade de pacotes capturados: {analisador.get_packet_count()}')
opcao2 = int(input('Deseja saber a quantidade de anomalias identificadas? \n 1 - Sim \n 2 - Não \n'))
if opcao2 == 1:
    print(f'Foram detectadas {analisador.identify_anomalies()} informações sobre o pacote que não estão disponíveis ou não podem ser determinadas.')

usuario.extract_data()