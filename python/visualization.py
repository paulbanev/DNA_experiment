import matplotlib.pyplot as plt


def plots(meanxsquares, MD, pr, meantransferrate):
    # First plot: mean probabilities per site (bar plot)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(1, MD + 1), meanxsquares)
    ax.set_ylabel(r'mean probability', fontsize=30)
    ax.set_xlabel(r'site', fontsize=30)
    ax.tick_params(axis='both', labelsize=18)
    ax.grid(True)
    fig.tight_layout()
    plt.show()

    # Second plot: participation ratio (line + dots)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(range(1, len(pr) + 1), pr, marker='o', linestyle='-', color='b')
    ax2.set_xlabel('Eigenvector index', fontsize=14)
    ax2.set_ylabel('Participation Ratio (PR)', fontsize=14)
    ax2.set_title('Participation Ratio per Eigenstate', fontsize=16)
    ax2.grid(True)
    fig2.tight_layout()
    plt.show()

    # Third plot: mean transfer rate per site
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(range(1, len(meantransferrate) + 1), meantransferrate, marker='o', linestyle='-', color='b')
    ax3.set_yscale('log')  # Set y-axis to logarithmic scale
    ax3.set_xlabel('Site', fontsize=14)
    ax3.set_ylabel('Mean Transfer Rate (log scale)', fontsize=14)
    ax3.set_title('Mean Transfer Rate per Site', fontsize=16)
    ax3.grid(True, which="both", ls='--', linewidth=0.5)
    fig3.tight_layout()
    plt.show()

    return fig, fig2, fig3  # Optional: return the figure object if needed

