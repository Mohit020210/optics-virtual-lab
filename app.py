import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

# Configure Page
st.set_page_config(page_title="Optics Virtual Lab - Class 12", layout="wide")
st.title("🔬 Class 12 Physics: Optics Virtual Lab")
st.caption("Interactive simulations with Olabs-style ray diagrams and auto-scaled optics.")

tab_mirror, tab_lens, tab_prism = st.tabs(["🪞 Spherical Mirror", "🔍 Spherical Lens", "🔺 Prism"])

# ==========================================
# TAB 1: SPHERICAL MIRRORS
# ==========================================
with tab_mirror:
    st.header("Spherical Mirror Ray Simulation")
    col_ctrl, col_diag = st.columns([1, 2])
    
    with col_ctrl:
        m_type = st.selectbox("Mirror Type:", ["Concave", "Convex"])
        u_mag = st.slider("Object Distance |u| (cm):", 5.0, 80.0, 30.0, 1.0)
        f_mag = st.slider("Focal Length |f| (cm):", 5.0, 40.0, 15.0, 1.0)
        ho = st.slider("Object Height (cm):", 1.0, 15.0, 5.0, 0.5)
        
        # Cartesian Sign Convention
        u = -u_mag
        f = -f_mag if m_type == "Concave" else f_mag
        
        # Mirror Formula: 1/v = 1/f - 1/u
        denom = (u - f)
        at_focus = abs(denom) < 0.1
        
        if not at_focus:
            v = (u * f) / denom
            m = -v / u
            hi = m * ho
            nature = "Virtual & Erect" if v > 0 else "Real & Inverted"
        else:
            v, m, hi = float('inf'), float('inf'), float('inf')
            nature = "At Infinity (Extremely Enlarged)"

        st.markdown("---")
        st.subheader("Calculated Output:")
        st.metric("Image Distance (v)", f"{v:.2f} cm" if not at_focus else "∞")
        st.metric("Magnification (m)", f"{m:.2f}" if not at_focus else "∞")
        st.metric("Image Height (hi)", f"{hi:.2f} cm" if not at_focus else "∞")
        st.info(f"**Nature:** {nature}")

    with col_diag:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.axhline(0, color='black', linewidth=1.2, linestyle='-') # Principal Axis
        
        # Viewport boundaries
        v_clamped = min(max(v if not at_focus else -100, -120), 120)
        hi_clamped = min(max(hi if not at_focus else -50, -40), 40)
        x_min = min(-u_mag - 15, v_clamped - 15, -2 * f_mag - 10)
        x_max = max(20, v_clamped + 15 if v_clamped > 0 else 20)
        y_max = max(ho, abs(hi_clamped), 10) * 1.5
        
        # Draw Mirror Curve
        y_curve = np.linspace(-y_max * 0.85, y_max * 0.85, 100)
        curvature_scale = 120.0
        x_curve = -np.square(y_curve) / curvature_scale if m_type == "Concave" else np.square(y_curve) / curvature_scale
        ax.plot(x_curve, y_curve, color='#1f77b4', linewidth=4, label=f'{m_type} Mirror')
        ax.axvline(0, color='gray', linestyle=':', linewidth=0.8)
        
        # Mark Focus (F) and Center of Curvature (C)
        ax.plot([f], [0], 'ko', markersize=5)
        ax.text(f, -y_max*0.12, 'F', fontsize=11, fontweight='bold', ha='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))
        ax.plot([2*f], [0], 'ko', markersize=5)
        ax.text(2*f, -y_max*0.12, 'C', fontsize=11, fontweight='bold', ha='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))

        # Draw Object Arrow
        ax.annotate('', xy=(u, ho), xytext=(u, 0), arrowprops=dict(arrowstyle="->", color='#d62728', lw=2.5))
        ax.text(u, ho + y_max*0.06, f'Object\n({abs(u):.0f}cm)', color='#d62728', ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#d62728", alpha=0.8))
        
        # Draw Image Arrow and Rays
        if not at_focus:
            ax.annotate('', xy=(v, hi), xytext=(v, 0), arrowprops=dict(arrowstyle="->", color='#2ca02c', lw=2.5))
            ax.text(v, hi - y_max*0.12 if hi < 0 else hi + y_max*0.06, f'Image\n({v:.1f}cm)', color='#2ca02c', ha='center', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2ca02c", alpha=0.8))
            
            # Parallel Ray
            ax.plot([u, 0], [ho, ho], color='orange', linestyle='--', lw=1.2)
            if v < 0:
                ax.plot([0, v], [ho, hi], color='orange', lw=1.2)
            else:
                ax.plot([0, -20], [ho, ho + (ho - 0)/(0 - f)*(-20)], color='orange', lw=1.2)
                ax.plot([0, v], [ho, hi], color='orange', linestyle=':', lw=1.2)

            # Pole Ray
            ax.plot([u, 0], [ho, 0], color='purple', linestyle='--', lw=1.2)
            if v < 0:
                ax.plot([0, v], [0, hi], color='purple', lw=1.2)
            else:
                ax.plot([0, -20], [0, -(-ho/u)*(-20)], color='purple', lw=1.2)
                ax.plot([0, v], [0, hi], color='purple', linestyle=':', lw=1.2)

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(-y_max, y_max)
        ax.set_xlabel("Distance along Principal Axis (cm)")
        ax.set_ylabel("Height (cm)")
        ax.grid(True, linestyle=':', alpha=0.6)
        st.pyplot(fig)


# ==========================================
# TAB 2: SPHERICAL LENSES
# ==========================================
with tab_lens:
    st.header("Spherical Lens Ray Simulation")
    col_ctrl_l, col_diag_l = st.columns([1, 2])
    
    with col_ctrl_l:
        l_type = st.selectbox("Lens Type:", ["Convex", "Concave"])
        u_mag_l = st.slider("Object Distance |u| (cm):", 5.0, 80.0, 35.0, 1.0, key="lens_u")
        f_mag_l = st.slider("Focal Length |f| (cm):", 5.0, 40.0, 20.0, 1.0, key="lens_f")
        ho_l = st.slider("Object Height (cm):", 1.0, 15.0, 6.0, 0.5, key="lens_ho")
        
        # Cartesian Sign Convention
        u_l = -u_mag_l
        f_l = f_mag_l if l_type == "Convex" else -f_mag_l
        
        # Lens Formula: 1/v = 1/f + 1/u
        denom_l = (u_l + f_l)
        at_focus_l = abs(denom_l) < 0.1
        
        if not at_focus_l:
            v_l = (u_l * f_l) / denom_l
            m_l = v_l / u_l
            hi_l = m_l * ho_l
            nature_l = "Real & Inverted" if v_l > 0 else "Virtual & Erect"
        else:
            v_l, m_l, hi_l = float('inf'), float('inf'), float('inf')
            nature_l = "At Infinity (Extremely Enlarged)"

        st.markdown("---")
        st.subheader("Calculated Output:")
        st.metric("Image Distance (v)", f"{v_l:.2f} cm" if not at_focus_l else "∞")
        st.metric("Magnification (m)", f"{m_l:.2f}" if not at_focus_l else "∞")
        st.metric("Image Height (hi)", f"{hi_l:.2f} cm" if not at_focus_l else "∞")
        st.info(f"**Nature:** {nature_l}")

    with col_diag_l:
        fig2, ax2 = plt.subplots(figsize=(9, 4.5))
        ax2.axhline(0, color='black', linewidth=1.2)
        
        # Safe Viewport Limits
        v_clamped_l = min(max(v_l if not at_focus_l else 100, -120), 120)
        hi_clamped_l = min(max(hi_l if not at_focus_l else -40, -40), 40)
        x_lim = max(u_mag_l + 15, abs(v_clamped_l) + 15, 2*f_mag_l + 10)
        y_lim = max(ho_l, abs(hi_clamped_l), 10) * 1.5
        
        # Draw Lens
        ax2.axvline(0, color='#1f77b4', linewidth=3, label=f'{l_type} Lens')
        ax2.plot(0, y_lim*0.85, '^' if l_type == "Convex" else 'v', color='#1f77b4', markersize=10)
        ax2.plot(0, -y_lim*0.85, 'v' if l_type == "Convex" else '^', color='#1f77b4', markersize=10)

        # Mark Focal Points
        for pos, name in [(-f_mag_l, 'F1'), (f_mag_l, 'F2'), (-2*f_mag_l, '2F1'), (2*f_mag_l, '2F2')]:
            ax2.plot(pos, 0, 'ko', markersize=4)
            ax2.text(pos, -y_lim*0.12, name, fontsize=10, ha='center',
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))

        # Object Arrow
        ax2.annotate('', xy=(u_l, ho_l), xytext=(u_l, 0), arrowprops=dict(arrowstyle="->", color='#d62728', lw=2.5))
        ax2.text(u_l, ho_l + y_lim*0.06, f'Object\n({abs(u_l):.0f}cm)', color='#d62728', ha='center', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#d62728", alpha=0.8))

        # Image Arrow and Rays
        if not at_focus_l:
            ax2.annotate('', xy=(v_l, hi_l), xytext=(v_l, 0), arrowprops=dict(arrowstyle="->", color='#2ca02c', lw=2.5))
            ax2.text(v_l, hi_l - y_lim*0.12 if hi_l < 0 else hi_l + y_lim*0.06, f'Image\n({v_l:.1f}cm)', color='#2ca02c', ha='center', fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2ca02c", alpha=0.8))
            
            # Parallel Ray
            ax2.plot([u_l, 0], [ho_l, ho_l], color='orange', linestyle='--', lw=1.2)
            if v_l > 0:
                ax2.plot([0, v_l], [ho_l, hi_l], color='orange', lw=1.2)
            else:
                ax2.plot([0, 30], [ho_l, ho_l + (hi_l - ho_l)/(v_l - 0)*(30)], color='orange', lw=1.2)
                ax2.plot([0, v_l], [ho_l, hi_l], color='orange', linestyle=':', lw=1.2)

            # Optical Center Ray
            ax2.plot([u_l, 0], [ho_l, 0], color='purple', linestyle='--', lw=1.2)
            if v_l > 0:
                ax2.plot([0, v_l], [0, hi_l], color='purple', lw=1.2)
            else:
                ax2.plot([0, 30], [0, (hi_l/v_l)*30], color='purple', lw=1.2)
                ax2.plot([0, v_l], [0, hi_l], color='purple', linestyle=':', lw=1.2)

        ax2.set_xlim(-x_lim, x_lim)
        ax2.set_ylim(-y_lim, y_lim)
        ax2.set_xlabel("Distance along Principal Axis (cm)")
        ax2.set_ylabel("Height (cm)")
        ax2.grid(True, linestyle=':', alpha=0.6)
        st.pyplot(fig2)


# ==========================================
# TAB 3: GLASS PRISM
# ==========================================
with tab_prism:
    st.header("Refraction Through Prism (Class 12 NCERT / Olabs)")
    col_p_ctrl, col_p_diag = st.columns([1, 2])
    
    with col_p_ctrl:
        A = st.slider("Angle of Prism (A) in degrees:", 30.0, 75.0, 60.0, 1.0)
        n = st.slider("Refractive Index (n):", 1.20, 2.00, 1.50, 0.01)
        i = st.slider("Angle of Incidence (i) in degrees:", 20.0, 75.0, 45.0, 1.0)
        
        # Snell's Law & Refraction Calculations
        r1 = math.degrees(math.asin(math.sin(math.radians(i)) / n))
        r2 = A - r1
        critical_angle = math.degrees(math.asin(1.0 / n))
        
        is_tir = r2 >= critical_angle
        
        if not is_tir:
            e = math.degrees(math.asin(n * math.sin(math.radians(r2))))
            delta = i + e - A
            delta_m = 2 * math.degrees(math.asin(n * math.sin(math.radians(A / 2.0)))) - A
            
            st.markdown("---")
            st.subheader("Calculated Output:")
            st.write(f"**Angle of Incidence ($i$):** {i:.1f}°")
            st.write(f"**Refraction angle 1 ($r_1$):** {r1:.2f}°")
            st.write(f"**Refraction angle 2 ($r_2$):** {r2:.2f}°")
            st.write(f"**Angle of Emergence ($e$):** {e:.2f}°")
            st.success(f"**Angle of Deviation ($\delta$):** {delta:.2f}°")
            st.info(f"**Minimum Deviation ($\delta_m$):** {delta_m:.2f}°")
        else:
            st.error(f"⚠️ Total Internal Reflection occurs at face 2! ($r_2 = {r2:.1f}^\circ$ > Critical Angle = {critical_angle:.1f}^\circ)")

    with col_p_diag:
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        
        # Geometry of the Prism
        H = 8.0
        half_base = H * math.tan(math.radians(A / 2.0))
        apex = np.array([0.0, H])
        left_base = np.array([-half_base, 0.0])
        right_base = np.array([half_base, 0.0])
        
        # Draw Glass Prism
        prism_poly = plt.Polygon([left_base, right_base, apex], closed=True, 
                                 facecolor='#edf7fa', edgecolor='#1f77b4', linewidth=2.5)
        ax3.add_patch(prism_poly)
        
        # Slant face directions and normal angles
        face_left_angle = math.atan2(apex[1] - left_base[1], apex[0] - left_base[0])
        face_right_angle = math.atan2(right_base[1] - apex[1], right_base[0] - apex[0])
        
        norm_left_angle = face_left_angle + math.pi / 2.0
        norm_right_angle = face_right_angle + math.pi / 2.0
        
        p_in = left_base + 0.5 * (apex - left_base)
        
        # Incident Ray
        ray_len = 5.0
        inc_dir = norm_left_angle - math.pi + math.radians(i)
        p_start = p_in - ray_len * np.array([math.cos(inc_dir), math.sin(inc_dir)])
        
        ax3.plot([p_start[0], p_in[0]], [p_start[1], p_in[1]], color='red', lw=2.2, label='Incident')
        ax3.annotate('', xy=(p_in[0], p_in[1]), xytext=(p_start[0], p_start[1]),
                     arrowprops=dict(arrowstyle="-|>", color='red', lw=2))
        
        # Normal 1
        n_len = 2.5
        norm_in_p1 = p_in + n_len * np.array([math.cos(norm_left_angle), math.sin(norm_left_angle)])
        norm_in_p2 = p_in - n_len * np.array([math.cos(norm_left_angle), math.sin(norm_left_angle)])
        ax3.plot([norm_in_p1[0], norm_in_p2[0]], [norm_in_p1[1], norm_in_p2[1]], 'k--', lw=1, alpha=0.6)

        # Refracted Ray inside prism
        p_out = right_base + 0.5 * (apex - right_base)
        ax3.plot([p_in[0], p_out[0]], [p_in[1], p_out[1]], color='orange', lw=2.2, label='Refracted')

        # Normal 2
        norm_out_p1 = p_out + n_len * np.array([math.cos(norm_right_angle), math.sin(norm_right_angle)])
        norm_out_p2 = p_out - n_len * np.array([math.cos(norm_right_angle), math.sin(norm_right_angle)])
        ax3.plot([norm_out_p1[0], norm_out_p2[0]], [norm_out_p1[1], norm_out_p2[1]], 'k--', lw=1, alpha=0.6)

        if not is_tir:
            em_dir = norm_right_angle - math.radians(e)
            p_end = p_out + ray_len * np.array([math.cos(em_dir), math.sin(em_dir)])
            
            ax3.plot([p_out[0], p_end[0]], [p_out[1], p_end[1]], color='green', lw=2.2, label='Emergent')
            ax3.annotate('', xy=(p_end[0], p_end[1]), xytext=(p_out[0], p_out[1]),
                         arrowprops=dict(arrowstyle="-|>", color='green', lw=2))
            
            ext_len = 4.0
            p_ext_inc = p_in + ext_len * np.array([math.cos(inc_dir), math.sin(inc_dir)])
            p_ext_em = p_out - ext_len * np.array([math.cos(em_dir), math.sin(em_dir)])
            ax3.plot([p_in[0], p_ext_inc[0]], [p_in[1], p_ext_inc[1]], 'r:', lw=1.2, alpha=0.7)
            ax3.plot([p_out[0], p_ext_em[0]], [p_out[1], p_ext_em[1]], 'g:', lw=1.2, alpha=0.7)

            ax3.text(p_start[0] - 0.4, p_start[1] + 0.3, f"i = {i:.0f}°", color='red', fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="red", alpha=0.9))
            ax3.text(p_end[0] + 0.4, p_end[1] - 0.3, f"e = {e:.1f}°", color='green', fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="green", alpha=0.9))

        ax3.text(0, H + 0.6, f"A = {A:.0f}°", color='#1f77b4', fontsize=12, fontweight='bold', ha='center',
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#1f77b4", alpha=0.9))
        ax3.text(0, H * 0.25, f"Glass Prism\nn = {n:.2f}", color='#333333', fontsize=11, ha='center',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#d8ecf8", ec="none", alpha=0.8))

        ax3.set_xlim(-half_base - 6, half_base + 6)
        ax3.set_ylim(-1.5, H + 2.0)
        ax3.axis('off')
        st.pyplot(fig3)
