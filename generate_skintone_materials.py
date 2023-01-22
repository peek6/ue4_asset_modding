# Script to automatically generate materials for various skincolors based on a template material
# Author:  peek6

import uasset_crc_gen


def to_bytes(my_str):
    return my_str.encode('UTF-8')


hack_uasset=True
hack_uexp=True


mi_path = '/Game/Coda/Character/Biped/HeroicFemale/_Model/_Materials/'

ssp_path = '/Game/Coda/Character/Biped/Shared/SSP/Hunter/'
ssp_prefix = 'SP_0'

num_tones = 15

template_tone = 9
template_tone_str = '09'

# grabbed by inspection of the SP_*.uexp in Game\Coda\Character\Biped\Shared\SSP\Hunter, typically at address 0xD0
# 1 and 9 have explicit colors at address 0x60
rgb_color_bytes = {
    1: bytes([0x23,0x86,0x15,0x3F,0x29,0x3D,0xC3,0x3E,0x42,0x27,0x9C,0x3E]),
    2: bytes([0x10,0x7A,0xB6,0x3E,0x77,0xA2,0x8C,0x3E,0x6C,0xCB,0x60,0x3E]),
    3: bytes([0x42,0x27,0x9C,0x3E,0x90,0x30,0x84,0x3E,0x36,0x20,0x82,0x3E]),
    4: bytes([0xE8,0x12,0xBE,0x3E,0xD0,0x5F,0x88,0x3E,0x83,0x18,0x78,0x3E]),
    5: bytes([0x42,0x27,0x9C,0x3E,0x1B,0x47,0x6C,0x3E,0x26,0x54,0x40,0x3E]),
    6: bytes([0x90,0x30,0x84,0x3E,0xB2,0x64,0x4E,0x3E,0x04,0xE7,0x3C,0x3E]),
    7: bytes([0xE7,0xE0,0x99,0x3E,0x9B,0x1E,0x74,0x3E,0x46,0x28,0x36,0x3E]),
    8: bytes([0xB7,0x7E,0x8A,0x3E,0x26,0x54,0x40,0x3E,0x4A,0x96,0x13,0x3E]),
    9: bytes([0x90,0x30,0x84,0x3E,0xB5,0x4E,0x2C,0x3E,0x5F,0x42,0x05,0x3E]),
    10: bytes([0xB2,0x64,0x4E,0x3E,0x8D,0x0E,0x08,0x3E,0xFD,0x83,0xA8,0x3D]),
    11: bytes([0xB5,0x4E,0x2C,0x3E,0xE6,0x5C,0xEA,0x3D,0xE7,0x18,0x90,0x3D]),
    12: bytes([0x1D,0x8F,0x19,0x3E,0xB1,0xDB,0xC7,0x3D,0x36,0x73,0x88,0x3D]),
    13: bytes([0x7E,0x8E,0xEF,0x3D,0x82,0xFD,0x97,0x3D,0x4D,0x4E,0x2D,0x3D]),
    14: bytes([0xB1,0xDB,0xC7,0x3D,0x79,0xE6,0x65,0x3D,0xF8,0x54,0xCE,0x3C]),
    15: bytes([0xFD,0x83,0xA8,0x3D,0x71,0xFF,0x51,0x3D,0xD4,0x99,0xFB,0x3C])
}

for tone in range(1, num_tones+1):
    if not(tone == template_tone):
        for mat_type in ['Lo', 'Up']:
            tone_str = str(tone)
            if(tone<10):
                tone_str = '0'+tone_str

            mi_prefix = 'MI_HR_HeroicFemale_Nude'+mat_type

            #create the strings to find in the template and the strings to replace them with
            template_mi_prefix = mi_prefix+template_tone_str
            target_mi_prefix = mi_prefix+tone_str

            template_ssp_prefix = ssp_prefix+template_tone_str
            target_ssp_prefix = ssp_prefix+tone_str

            template_mi_uasset = template_mi_prefix+'.uasset'
            target_mi_uasset = target_mi_prefix+'.uasset'

            template_ssp_uasset = template_ssp_prefix + '.uasset'
            target_ssp_uasset = target_ssp_prefix + '.uasset'


            # open the template uasset
            fin = open(template_mi_uasset, "rb")
            data = fin.read()

            # replace the strings
            replace_set = []

            replace_set.append((mi_path+template_mi_prefix, mi_path+target_mi_prefix))
            replace_set.append((ssp_path+template_ssp_prefix, ssp_path+target_ssp_prefix))
            replace_set.append((template_mi_prefix, target_mi_prefix))
            replace_set.append((template_ssp_prefix,target_ssp_prefix))

            for replace_iter in range(len(replace_set)):
                # replace the actual string
                data = data.replace(to_bytes(replace_set[replace_iter][0]),to_bytes(replace_set[replace_iter][1]))
                # replace the string's hash
                template_hash = uasset_crc_gen.GenerateHash(replace_set[replace_iter][0])
                target_hash = uasset_crc_gen.GenerateHash(replace_set[replace_iter][1])
                data = data.replace(template_hash, target_hash)  # TODO:  Maybe dangerous if this pattern appears elsewhere in file for some reason.  Hopefully unlikely.

            fin.close()


            # Hack the target uasset
            if(hack_uasset):
                fout = open(target_mi_uasset, "wb")
                fout.write(data)
                fout.close()



            template_mi_uexp = template_mi_prefix+'.uexp'
            target_mi_uexp = target_mi_prefix+'.uexp'


            # find the RGB info in the template uasset
            fin = open(template_mi_uexp, "rb")
            data = fin.read()
            rgb_loc = data.find(rgb_color_bytes[template_tone])
            fin.close()

            data = data.replace(rgb_color_bytes[template_tone], rgb_color_bytes[tone])

            if(hack_uexp):
                fout = open(target_mi_uexp, "wb")
                fout.write(data)
                fout.close()


            #with fin as open(template_mi_uexp,'rb'):
            #    data = fin.read()
            #    data.seek(rgb_color_strings[9])





