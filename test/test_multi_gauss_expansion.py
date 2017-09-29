"""
Tests for `galkin` module.
"""
import pytest
import numpy.testing as npt
import astrofunc.multi_gauss_expansion as mge
import numpy as np
from lenstronomy.ImSim.light_model import LightModel
from lenstronomy.ImSim.lens_model import LensModel
from galkin.galkin import Galkin


class TestGalkin(object):

    def setup(self):
        pass

    def test_mge_hernquist_light(self):
        """
        compare power-law profiles analytical vs. numerical
        :return:
        """
        # anisotropy profile
        anisotropy_type = 'OsipkovMerritt'
        r_ani = 2.
        kwargs_anisotropy = {'r_ani': r_ani}  # anisotropy radius [arcsec]

        # aperture as slit
        aperture_type = 'slit'
        length = 3.8
        width = 0.9
        kwargs_aperture = {'length': length, 'width': width, 'center_ra': 0, 'center_dec': 0, 'angle': 0}

        psf_fwhm = 0.7  # Gaussian FWHM psf
        kwargs_cosmo = {'D_d': 1000, 'D_s': 1500, 'D_ds': 800}

        # light profile
        light_profile_list = ['HERNQUIST']
        r_eff = 1.8
        kwargs_light = [{'Rs':  r_eff, 'sigma0': 1.}]  # effective half light radius (2d projected) in arcsec

        # mge of light profile
        lightModel = LightModel(light_profile_list)
        r_array = np.logspace(-2, 2, 100)
        flux_r = lightModel.surface_brightness(r_array, 0, kwargs_light)
        amps, sigmas, norm = mge.mge_1d(r_array, flux_r, N=20)
        light_profile_list_mge = ['MULTI_GAUSSIAN']
        kwargs_light_mge = [{'amp': amps, 'sigma': sigmas}]

        # mass profile
        mass_profile_list = ['SPP']
        theta_E = 1.2
        gamma = 2.
        kwargs_profile = [{'theta_E': theta_E, 'gamma': gamma}]  # Einstein radius (arcsec) and power-law slope

        galkin = Galkin(mass_profile_list, light_profile_list, aperture_type=aperture_type, anisotropy_model=anisotropy_type, fwhm=psf_fwhm, kwargs_cosmo=kwargs_cosmo)
        sigma_v = galkin.vel_disp(kwargs_profile, kwargs_light, kwargs_anisotropy, kwargs_aperture, num=1000)

        galkin = Galkin(mass_profile_list, light_profile_list_mge, aperture_type=aperture_type, anisotropy_model=anisotropy_type, fwhm=psf_fwhm, kwargs_cosmo=kwargs_cosmo)
        sigma_v2 = galkin.vel_disp(kwargs_profile, kwargs_light_mge, kwargs_anisotropy, kwargs_aperture, num=1000)

        print sigma_v, sigma_v2, 'sigma_v Galkin, sigma_v MGEn'
        print (sigma_v/sigma_v2)**2

        npt.assert_almost_equal((sigma_v-sigma_v2)/sigma_v2, 0, decimal=2)

    def test_mge_power_law_lens(self):
        """
        compare power-law profiles analytical vs. numerical
        :return:
        """
        # anisotropy profile
        anisotropy_type = 'OsipkovMerritt'
        r_ani = 2.
        kwargs_anisotropy = {'r_ani': r_ani}  # anisotropy radius [arcsec]

        # aperture as slit
        aperture_type = 'slit'
        length = 3.8
        width = 0.9
        kwargs_aperture = {'length': length, 'width': width, 'center_ra': 0, 'center_dec': 0, 'angle': 0}

        psf_fwhm = 0.7  # Gaussian FWHM psf
        kwargs_cosmo = {'D_d': 1000, 'D_s': 1500, 'D_ds': 800}

        # light profile
        light_profile_list = ['HERNQUIST']
        r_eff = 1.8
        kwargs_light = [{'Rs':  r_eff, 'sigma0': 1.}]  # effective half light radius (2d projected) in arcsec

        # mass profile
        mass_profile_list = ['SPP']
        theta_E = 1.2
        gamma = 2.
        kwargs_profile = [{'theta_E': theta_E, 'gamma': gamma}]  # Einstein radius (arcsec) and power-law slope

        # mge of lens profile
        lensModel = LensModel(kwargs_options={'lens_model_list': mass_profile_list})
        r_array = np.logspace(-2, 2, 100)
        kappa_r = lensModel.kappa(r_array, 0, kwargs_profile)
        amps, sigmas, norm = mge.mge_1d(r_array, kappa_r, N=20)
        mass_profile_list_mge = ['MULTI_GAUSSIAN_KAPPA']
        kwargs_profile_mge = [{'amp': amps, 'sigma': sigmas}]


        galkin = Galkin(mass_profile_list, light_profile_list, aperture_type=aperture_type, anisotropy_model=anisotropy_type, fwhm=psf_fwhm, kwargs_cosmo=kwargs_cosmo)
        sigma_v = galkin.vel_disp(kwargs_profile, kwargs_light, kwargs_anisotropy, kwargs_aperture, num=1000)

        galkin = Galkin(mass_profile_list_mge, light_profile_list, aperture_type=aperture_type, anisotropy_model=anisotropy_type, fwhm=psf_fwhm, kwargs_cosmo=kwargs_cosmo)
        sigma_v2 = galkin.vel_disp(kwargs_profile_mge, kwargs_light, kwargs_anisotropy, kwargs_aperture, num=1000)

        print sigma_v, sigma_v2, 'sigma_v Galkin, sigma_v MGEn'
        print (sigma_v/sigma_v2)**2

        npt.assert_almost_equal((sigma_v-sigma_v2)/sigma_v2, 0, decimal=2)

    def test_mge_light_and_mass(self):
        # anisotropy profile
        anisotropy_type = 'OsipkovMerritt'
        r_ani = 2.
        kwargs_anisotropy = {'r_ani': r_ani}  # anisotropy radius [arcsec]

        # aperture as slit
        aperture_type = 'slit'
        length = 3.8
        width = 0.9
        kwargs_aperture = {'length': length, 'width': width, 'center_ra': 0, 'center_dec': 0, 'angle': 0}

        psf_fwhm = 0.7  # Gaussian FWHM psf
        kwargs_cosmo = {'D_d': 1000, 'D_s': 1500, 'D_ds': 800}

        # light profile
        light_profile_list = ['HERNQUIST']
        r_eff = 1.8
        kwargs_light = [{'Rs':  r_eff, 'sigma0': 1.}]  # effective half light radius (2d projected) in arcsec

        # mass profile
        mass_profile_list = ['SPP']
        theta_E = 1.2
        gamma = 2.
        kwargs_profile = [{'theta_E': theta_E, 'gamma': gamma}]  # Einstein radius (arcsec) and power-law slope

        # mge of light profile
        lightModel = LightModel(light_profile_list)
        r_array = np.logspace(-2, 2, 100)
        flux_r = lightModel.surface_brightness(r_array, 0, kwargs_light)
        amps, sigmas, norm = mge.mge_1d(r_array, flux_r, N=20)
        light_profile_list_mge = ['MULTI_GAUSSIAN']
        kwargs_light_mge = [{'amp': amps, 'sigma': sigmas}]

        # mge of lens profile
        lensModel = LensModel(kwargs_options={'lens_model_list': mass_profile_list})
        r_array = np.logspace(-2, 2, 100)
        kappa_r = lensModel.kappa(r_array, 0, kwargs_profile)
        amps, sigmas, norm = mge.mge_1d(r_array, kappa_r, N=20)
        mass_profile_list_mge = ['MULTI_GAUSSIAN_KAPPA']
        kwargs_profile_mge = [{'amp': amps, 'sigma': sigmas}]


        galkin = Galkin(mass_profile_list, light_profile_list, aperture_type=aperture_type, anisotropy_model=anisotropy_type, fwhm=psf_fwhm, kwargs_cosmo=kwargs_cosmo)
        sigma_v = galkin.vel_disp(kwargs_profile, kwargs_light, kwargs_anisotropy, kwargs_aperture, num=1000)

        galkin = Galkin(mass_profile_list_mge, light_profile_list_mge, aperture_type=aperture_type, anisotropy_model=anisotropy_type, fwhm=psf_fwhm, kwargs_cosmo=kwargs_cosmo)
        sigma_v2 = galkin.vel_disp(kwargs_profile_mge, kwargs_light_mge, kwargs_anisotropy, kwargs_aperture, num=1000)

        print sigma_v, sigma_v2, 'sigma_v Galkin, sigma_v MGEn'
        print (sigma_v/sigma_v2)**2

        npt.assert_almost_equal((sigma_v-sigma_v2)/sigma_v2, 0, decimal=2)

if __name__ == '__main__':
    pytest.main()