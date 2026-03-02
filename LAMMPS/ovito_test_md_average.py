from ovito_tools import gr_timeaveraged,gr_kde_from_ovito_new,gr_from_csv,gr_single_frame
from pathlib import Path
import matplotlib.pyplot as plt
PROJECT_ROOT = Path(__file__).resolve().parents[0]

pot1 = "20260212_152203"
pot2 = "20260223_154848"
paper_sol=gr_from_csv("correct_literature_rdf")
paper_liq=gr_from_csv("liquid_rdf")
sigma=0.1
new_sol=gr_timeaveraged(pot2,i_start=700,i_end=800,cutoff=11,n_bins=200)
new_liq=gr_timeaveraged(pot2,i_start=10,i_end=300,cutoff=11,n_bins=200)
#first=gr_single_frame(pot2, frame=700,n_bins=200)
#last=gr_single_frame(pot2, frame=800,n_bins=200)
#first=gr_kde_from_ovito_new(pot2,frame=800,cutoff=11,n_bins=200,sigma=sigma)

fig, ax = plt.subplots(figsize=(6,4))
# ax.plot(r1, gr1, label="simulated liquid",color='red')
# ax.plot(r2, gr2, label="simulated amorphous",color="blue",alpha=0.5)

#ax.plot(old[0], old[1], label="old potential",)
ax.plot(new_liq[0], new_liq[1], label="MD liquid",)
ax.plot(paper_liq[0],paper_liq[1],label="literature liquid",linestyle=":")
out_prefix = f"liquid"
# ax.plot(new_sol[0], new_sol[1], label="MD solid",)
# ax.plot(paper_sol[0],paper_sol[1],label="literature solid",linestyle=":")
# out_prefix = f"solid"

# ax.plot(first[0],first[1],label="KDE")
# ax.plot(last[0],last[1],label="histogram")
# ax.plot(paper_sol[0],paper_sol[1],label="literature solid",linestyle=":")
# out_prefix=("first_last")
ax.set_xlim(2,10)
ax.set_ylim(0,4)
ax.set_xlabel("r (\u212B)")
ax.set_ylabel("g(r)")
ax.legend()
fig.tight_layout()
fig.savefig(f"{PROJECT_ROOT}/images/KDE_test_{out_prefix}.png", dpi=300, bbox_inches="tight")
plt.show()

