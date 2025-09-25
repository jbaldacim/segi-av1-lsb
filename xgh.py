from argparse import ArgumentParser
from PIL import Image
import numpy as np

END_MARKER = [0] * 8  # marcador de fim: byte 00000000

def hide_message(message, input_filepath, output_filepath):
    # Abrir imagem
    image = Image.open(input_filepath)
    image_np = np.array(image)

    # Transformar mensagem em bytes UTF-8
    message_bytes = message.encode('utf-8')
    message_bits = [int(b) for byte in message_bytes for b in f'{byte:08b}']

    # Adicionar marcador de fim
    message_bits += END_MARKER

    # Flatten do canal vermelho
    flat_red_channel = image_np[:, :, 0].flatten()

    if len(message_bits) > len(flat_red_channel):
        raise ValueError("Mensagem muito longa para a imagem selecionada.")

    # Inserir bits usando LSB
    flat_red_channel[:len(message_bits)] = (flat_red_channel[:len(message_bits)] & 254) | message_bits
    image_np[:, :, 0] = flat_red_channel.reshape(image_np[:, :, 0].shape)

    # Salvar imagem modificada
    Image.fromarray(image_np).save(output_filepath)
    print(f"Mensagem escondida em {output_filepath}")


def reveal_message(input_filepath):
    # Abrir imagem
    image = Image.open(input_filepath)
    image_np = np.array(image)

    # Flatten do canal vermelho
    flat_red_channel = image_np[:, :, 0].flatten()

    # Extrair LSBs
    lsb_bits = flat_red_channel & 1

    # Ler bytes até encontrar o marcador de fim
    message_bytes = []
    for i in range(0, len(lsb_bits), 8):
        byte_bits = lsb_bits[i:i+8]
        if len(byte_bits) < 8 or all(b == 0 for b in byte_bits):
            break
        byte_val = int(''.join(str(b) for b in byte_bits), 2)
        message_bytes.append(byte_val)

    # Decodificar bytes UTF-8
    message = bytes(message_bytes).decode('utf-8', errors='ignore')
    print("Mensagem revelada:")
    print(message)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('action', choices=['hide', 'reveal'], help="hide para esconder, reveal para revelar")
    parser.add_argument('input_filepath', help="Imagem de entrada")
    parser.add_argument('message', nargs='?', help="Mensagem a esconder (somente hide)")
    parser.add_argument('output_filepath', nargs='?', help="Arquivo de saída (somente hide)")
    args = parser.parse_args()

    if args.action == 'hide':
        if not args.message:
            parser.error("É necessário fornecer uma mensagem para esconder.")
        if not args.output_filepath:
            parser.error("É necessário fornecer um arquivo de saída.")

    return args


if __name__ == "__main__":
    args = parse_args()
    if args.action == 'hide':
        hide_message(args.message, args.input_filepath, args.output_filepath)
    elif args.action == 'reveal':
        reveal_message(args.input_filepath)