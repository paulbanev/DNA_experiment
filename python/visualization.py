import os
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def save_plots(results, output_dir="results"):
    """Save plots to disk (original function)"""
    os.makedirs(output_dir, exist_ok=True)

    # Convert lists to arrays
    idio=np.array(results["idiotimes"])
    pr = np.array(results["participation ratio"])
    mean_prob = np.array(results["pithanotites"])
    mean_trans = np.array(results["mean transfer rate"])
    dmx = np.array(results.get("x axis dipole moment", []))
    dmy = np.array(results.get("y axis dipole moment", []))
    mesithesi = np.array(results.get("mesi thesi", [])).ravel()
    count = np.array(results.get("count", [])).ravel()

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

    # --- Density of States (DOS) calculation and plot ---
    fig, ax = plt.subplots()
    ax.fill_between(mesithesi, count)
    ax.set_ylabel('DOS (a.u.)')
    ax.set_xlabel('Energy (eV)')
    ax.set_title("Density of States (DOS)")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "density_of_states.png"))
    plt.close(fig)


def generate_plots_svg(results):
    """Generate plots as SVG strings for web display (vector graphics - perfect zoom)"""
    plots = {}
    
    # Convert lists to arrays
    idio = np.array(results["idiotimes"])
    pr = np.array(results["participation ratio"])
    mean_prob = np.array(results["pithanotites"])
    mean_trans = np.array(results["mean transfer rate"])
    mesithesi = np.array(results.get("mesi thesi", [])).ravel()
    count = np.array(results.get("count", [])).ravel()

    pr_mean = np.mean(pr, axis=0)
    pr_err = np.std(pr, axis=0)
    mean_prob_mean = np.mean(mean_prob, axis=0)
    mean_prob_err = np.std(mean_prob, axis=0)
    mean_trans_mean = np.mean(mean_trans, axis=0)
    mean_trans_err = np.std(mean_trans, axis=0)

    x_vals = np.arange(1, len(pr_mean) + 1)

    # --- 1. Eigenvalue Spectrum ---
    if "idiotimes" in results:
        idio_mean = np.mean(idio, axis=0)
        idio_err = np.std(idio, axis=0)
        x_vals_eigen = np.arange(1, len(idio_mean) + 1)

        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        ax.errorbar(x_vals_eigen, idio_mean, yerr=idio_err, fmt='o', capsize=3, 
                   markersize=6, linewidth=2, elinewidth=2)
        ax.set_title("Eigenvalue Spectrum (Idiosynchronous Energies)", fontsize=14, fontweight='bold')
        ax.set_xlabel("Eigenstate Index", fontsize=12)
        ax.set_ylabel("Energy (eV)", fontsize=12)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        
        # Save as SVG to string
        svg_io = io.BytesIO()
        fig.savefig(svg_io, format='svg', bbox_inches='tight')
        svg_io.seek(0)
        plots['eigenvalue_spectrum'] = base64.b64encode(svg_io.read()).decode('utf-8')
        plt.close(fig)

    # --- 2. Participation Ratio ---
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.errorbar(x_vals, pr_mean, yerr=pr_err, fmt='-o', capsize=3, 
               markersize=6, linewidth=2, elinewidth=2)
    ax.set_title("Participation Ratio", fontsize=14, fontweight='bold')
    ax.set_xlabel("Eigenvector Index", fontsize=12)
    ax.set_ylabel("PR", fontsize=12)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    
    svg_io = io.BytesIO()
    fig.savefig(svg_io, format='svg', bbox_inches='tight')
    svg_io.seek(0)
    plots['participation_ratio'] = base64.b64encode(svg_io.read()).decode('utf-8')
    plt.close(fig)

    # --- 3. Mean Probabilities ---
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.bar(x_vals, mean_prob_mean, yerr=mean_prob_err, capsize=3, 
          alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_title("Mean Probability per Site", fontsize=14, fontweight='bold')
    ax.set_xlabel("Site Index", fontsize=12)
    ax.set_ylabel("Mean Probability", fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    fig.tight_layout()
    
    svg_io = io.BytesIO()
    fig.savefig(svg_io, format='svg', bbox_inches='tight')
    svg_io.seek(0)
    plots['mean_probability'] = base64.b64encode(svg_io.read()).decode('utf-8')
    plt.close(fig)

    # --- 4. Mean Transfer Rate ---
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.errorbar(x_vals, mean_trans_mean, yerr=mean_trans_err, fmt='-o', capsize=3, 
               markersize=6, linewidth=2, elinewidth=2)
    ax.set_yscale("log")
    ax.set_title("Mean Transfer Rate (log scale)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Site Index", fontsize=12)
    ax.set_ylabel("Transfer Rate", fontsize=12)
    ax.grid(True, which='both', ls='--', alpha=0.3)
    fig.tight_layout()
    
    svg_io = io.BytesIO()
    fig.savefig(svg_io, format='svg', bbox_inches='tight')
    svg_io.seek(0)
    plots['mean_transfer_rate'] = base64.b64encode(svg_io.read()).decode('utf-8')
    plt.close(fig)

    # --- 5. Density of States ---
    if len(mesithesi) > 0 and len(count) > 0:
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        ax.fill_between(mesithesi, count, alpha=0.6, linewidth=2, edgecolor='black')
        ax.set_ylabel('DOS (a.u.)', fontsize=12)
        ax.set_xlabel('Energy (eV)', fontsize=12)
        ax.set_title("Density of States (DOS)", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        
        svg_io = io.BytesIO()
        fig.savefig(svg_io, format='svg', bbox_inches='tight')
        svg_io.seek(0)
        plots['density_of_states'] = base64.b64encode(svg_io.read()).decode('utf-8')
        plt.close(fig)

    return plots