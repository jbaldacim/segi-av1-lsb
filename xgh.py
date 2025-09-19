from argparse import ArgumentParser
from PIL import Image
import numpy as np

image = Image.open('IFSP_logo.jpg')

image_np = np.array(image)

lsb = image_np & 1

red_lsb = lsb[:,:,0]


def bits_to_bytes(bits):
    # bits: array 1D ou 2D com bits (0 ou 1)
    bits = bits.flatten()
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        byte_str = ''.join(str(b) for b in byte)
        bytes_list.append(int(byte_str, 2))
    return bytes_list


def parse_args():
    parser = ArgumentParser()

    parser.add_argument(
        'action',
        choices=['reveal', 'hide'],
        help="Especificar se 'hide' para esconder a mensagem ou 'reveal' para exibir a mensagem"
    )

    parser.add_argument(
        'input_filepath',
        help='Caminho da imagem original'
    )

    parser.add_argument(
        'message',
        nargs='?',
        help="Se action='hide', mensagem a ser escondida"
    )

    parser.add_argument(
        'output_filepath',
        nargs='?',
        help="Se action='hide', nome do arquivo modificado"
    )

    args = parser.parse_args()

    if args.action == 'hide':
        if not args.message:
            parser.error("action='hide' requer um argumento message")
        if not args.output_filepath:
            parser.error("action='hide' requer um argumento output_filepath")

    return args


if __name__ == "__main__":
    # args = parse_args()
    # print(f'action={args.action}')
    # print(f'input_filepath={args.input_filepath}')
    # print(f'message: {args.message}')
    # print(f'output_filepath={args.output_filepath}')

    print("Bits extraídos (primeiros 64 bits):")
    print(len(red_lsb.flatten()))

