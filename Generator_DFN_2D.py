from PIL import Image
from PIL import ImageDraw
import numpy as np
from bgem.stochastic import fracture


# I have no idea how or why this works or what it´s used for, but it seems to change the scale somehow?
def scale_cut(x, s):
    return tuple([max(0, min(sv, int(sv * xv))) for xv, sv in zip(x[:2], s)])


# def compute_p_30_from_p_32(p_32, k_r, r_min, r_max):
#     """
#     Computes fracture intensity (p_30) from the mean fracture surface area per unit volume (p_32)
#     :param p_32: mean fracture surface area per unit volume
#     :param k_r: power law exponent
#     :param r_min: minimum radius/size of a fracture
#     :param r_max: maximum radius/size of a fracture
#     :return: p_30 - fracture intensity
#     """
#
#     # Area of the unit fracture shape (1 for square, 'pi/4' for disc)
#     shape_area = 1.0
#
#     integral_area = (r_max ** (2 - k_r) - r_min ** (2 - k_r)) / (2 - k_r)
#     integral_intensity = (r_max ** (-k_r) - r_min ** (-k_r)) / -k_r
#     p_30 = (p_32 * integral_intensity) / (integral_area * shape_area)
#     return p_30


# def power_law_instance_from_p_32(p_32, k_r, r_min, r_max):
#    """
#    Constructs the distribution using the mean area p_32 instead of intensity p_30
#    :param p_32: mean area of the fractures in given fracture_size_range
#    :return: PowerLawSize instance
#    """
#    fracture_size_range = (r_min, r_max)
#    p_30 = fracture.PowerLawSize.intensity_for_mean_area(p_32, k_r, r_min, r_max)
#    return fracture.PowerLawSize(k_r, fracture_size_range, p_30)


def plot_dfn(k_r, p_32, r_min, r_max):

    s = (1000, 1000)

    im = Image.new('RGBA', s, (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    fracture_box = [1, 1, 0]
    sample_range = (r_min, r_max)
    pop = fracture.Population(fracture_box[0] * fracture_box[1])
    conf_range = [r_min, r_max]
    #p_32 = 0.094
    size = fracture.PowerLawSize.from_mean_area(k_r - 1, conf_range, p_32, k_r)
    pop.add_family("all",
                   orientation=fracture.FisherOrientation(0, 90, 0),
                   shape=size,
                   shape_angle=fracture.VonMisesOrientation(0, 0)
                   )
    pop.set_sample_range(sample_range)
    pos_gen = fracture.UniformBoxPosition(fracture_box)
    fractures = pop.sample(pos_distr=pos_gen, keep_nonempty=True)
    sizes = []
    for fr in fractures:
        t = 0.5 * fr.r * np.array([-fr.normal[0][2], fr.normal[0][1], 0])
        a = scale_cut(0.5 + fr.center - t, s)
        b = scale_cut(0.5 + fr.center + t, s)
        draw.line((a, b), fill=(0,0,0), width=1)
        sizes.append(fr.r)

    #plot_sizes(sizes, sample_range, pop.families[0].size)

    #ax.imshow(np.asarray(im),  origin='lower')
    im.show()
    return pop.mean_size(),len(fractures)

