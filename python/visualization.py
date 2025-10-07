import os
import numpy as np
import matplotlib.pyplot as plt

def save_plots(results, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)

    # Convert lists to arrays
    idio=np.array(results["idiotimes"])
    pr = np.array(results["participation ratio"])
    mean_prob = np.array(results["pithanotites"])
    mean_trans = np.array(results["mean transfer rate"])
    dmx = np.array(results.get("x axis dipole moment", []))
    dmy = np.array(results.get("y axis dipole moment", []))
    mesithesi = np.array(results.get("mesi thesi", []))
    count = np.array(results.get("count", []))

    pr_mean = np.mean(pr, axis=0)
    pr_err = np.std(pr, axis=0)
    mean_prob_mean = np.mean(mean_prob, axis=0)
    mean_prob_err = np.std(mean_prob, axis=0)
    mean_trans_mean = np.mean(mean_trans, axis=0)
    mean_trans_err = np.std(mean_trans, axis=0)

    x_vals = np.arange(1, len(pr_mean) + 1)

    # --- Idiosynchronous Energies (Eigenvalues) ---
    if "idiotimes" in results:
        idio = np.array(results["idiotimes"])
        idio_mean = np.mean(idio, axis=0)
        idio_err = np.std(idio, axis=0)
        x_vals = np.arange(1, len(idio_mean) + 1)

        fig, ax = plt.subplots()
        ax.errorbar(x_vals, idio_mean, yerr=idio_err, fmt='o', capsize=3)
        ax.set_title("Eigenvalue Spectrum (Idiosynchronous Energies)")
        ax.set_xlabel("Eigenstate Index")
        ax.set_ylabel("Energy (eV)")
        ax.grid(True)
        fig.tight_layout()
        fig.savefig(os.path.join(output_dir, "eigenvalue_spectrum.png"))
        plt.close(fig)

    # --- Participation Ratio ---
    fig, ax = plt.subplots()
    ax.errorbar(x_vals, pr_mean, yerr=pr_err, fmt='-o', capsize=3)
    ax.set_title("Participation Ratio")
    ax.set_xlabel("Eigenvector Index")
    ax.set_ylabel("PR")
    ax.grid(True)
    fig.savefig(os.path.join(output_dir, "participation_ratio.png"))
    plt.close(fig)

    # --- Mean Probabilities ---
    fig, ax = plt.subplots()
    ax.bar(x_vals, mean_prob_mean, yerr=mean_prob_err, capsize=3)
    ax.set_title("Mean Probability per Site")
    ax.set_xlabel("Site Index")
    ax.set_ylabel("Mean Probability")
    ax.grid(True)
    fig.savefig(os.path.join(output_dir, "mean_probability.png"))
    plt.close(fig)

    # --- Mean Transfer Rate ---
    fig, ax = plt.subplots()
    ax.errorbar(x_vals, mean_trans_mean, yerr=mean_trans_err, fmt='-o', capsize=3)
    ax.set_yscale("log")
    ax.set_title("Mean Transfer Rate (log scale)")
    ax.set_xlabel("Site Index")
    ax.set_ylabel("Transfer Rate")
    ax.grid(True, which='both', ls='--')
    fig.savefig(os.path.join(output_dir, "mean_transfer_rate.png"))
    plt.close(fig)

    # --- Dipole Moment (if available) ---
    if dmx.size and dmy.size:
        dmx_mean = np.mean(dmx, axis=0)
        dmy_mean = np.mean(dmy, axis=0)
        fig, ax = plt.subplots()
        ax.plot(dmx_mean, label='dmx')
        ax.plot(dmy_mean, label='dmy')
        ax.set_title("Dipole Moment vs Time")
        ax.set_xlabel("Time Index")
        ax.set_ylabel("Dipole Moment [a.u.]")
        ax.legend()
        ax.grid(True)
        fig.savefig(os.path.join(output_dir, "dipole_moment.png"))
        plt.close(fig)
    
        # --- Density of States (DOS) calculation and plot ---
          # number of points for DOS bins; you can change this or make it input if you want
       # fig, ax = plt.subplots()
        #ax.fill_between(mesithesi, count)
        #ax.set_ylabel('DOS (a.u.)')
        #ax.set_xlabel('Energy (eV)')
        #ax.set_title("Density of States (DOS)")
        #ax.grid(True)
        #fig.tight_layout()
        #fig.savefig(os.path.join(output_dir, "density_of_states.png"))
        #plt.close(fig)