import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

# Configure Webpage Layout
st.set_page_config(page_title="Optics Virtual Lab - Class 12", layout="wide")
st.title("🔬 Class 12 Physics: Optics Virtual Lab")
st.caption("Interactive simulations with fixed-aperture optics, realistic ray tracing, and sign conventions.")

tab_mirror, tab_lens, tab_prism = st.tabs(["🪞 Spherical Mirror", "🔍 Spherical Lens", "🔺 Prism"])

# =========================================================
# TAB 1: SPHERICAL MIRROR
# =========================================================
with tab_mirror:
    st.header("Spherical Mirror Simulation")
    col_ctrl, col_diag = st.columns([1, 2])
    
    with col_ctrl:
        m_type = st.selectbox("Mirror Type:", ["Concave", "Convex"])
        u_mag = st.slider("Object Distance |u| (cm):", 5.0, 80.0, 30.0, 1.0)
        f_mag = st.slider("Focal Length |f| (cm):", 10.0, 40.0, 15.0, 1.0)
        ho = st.slider("Object Height (cm):", 1.0, 10.0, 4.0, 0.5)
        
        # Cartesian Sign Convention
        u = -u_mag
        f = -f_mag if m_type == "Concave" else f_mag
        
        # Mirror Formula: 1/v = 1/f - 1/u => v = (u*f)/(u-f)
        denom = u - f
        at_focus = abs(denom) < 0.2
        
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
        fig, ax = plt.subplots(figsize=(9, 4.8))
        
        # PERMANENTLY FIXED AXES & TICKS (Prevents all jumping/rescaling)
        X_MIN, X_MAX = -100.0, 30.0
        Y_MIN, Y_MAX = -15.0, 15.0
        ax.set_xlim(X_MIN, X_MAX)
        ax.set_ylim(Y_MIN, Y_MAX)
        ax.set_xticks(np.arange(-100, 31, 10))
        ax.set_yticks(np.arange(-15, 16, 5))
        ax.set_autoscale_on(False)
        
        ax.axhline(0, color='black', linewidth=1.2) # Principal Axis
        
        # Fixed physical mirror aperture
        MIRROR_HALF_HEIGHT = 10.0
        y_curve = np.linspace(-MIRROR_HALF_HEIGHT, MIRROR_HALF_HEIGHT, 100)
        
        # Curvature radius R = 2f
        R = 2.0 * f_mag
        x_curve = -np.square(y_curve) / (2.0 * R) if m_type == "Concave" else np.square(y_curve) / (2.0 * R)
        
        # Draw Mirror
        ax.plot(x_curve, y_curve, color='#1f77b4', linewidth=3.5, label='Mirror')
        
        # Silvered surface hatching
        hatch_dx = 0.6 if m_type == "Concave" else -0.6
        for y_pt in np.linspace(-MIRROR_HALF_HEIGHT + 0.5, MIRROR_HALF_HEIGHT - 0.5, 15):
            x_pt = - (y_pt**2)/(2.0*R) if m_type == "Concave" else (y_pt**2)/(2.0*R)
            ax.plot([x_pt, x_pt + hatch_dx], [y_pt, y_pt - 0.6], color='gray', lw=1)

        # Mark Focus (F) and Center of Curvature (C)
        ax.plot([f], [0], 'ko', markersize=5)
        ax.text(f, -1.8, 'F', fontsize=11, fontweight='bold', ha='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))
        ax.plot([2*f], [0], 'ko', markersize=5)
        ax.text(2*f, -1.8, 'C', fontsize=11, fontweight='bold', ha='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

        # Draw Object Arrow
        ax.annotate('', xy=(u, ho), xytext=(u, 0), arrowprops=dict(arrowstyle="->", color='#d62728', lw=2.5))
        ax.text(u, ho + 1.2, f'Object\n{ho:.1f}cm', color='#d62728', ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#d62728", alpha=0.85))

        if not at_focus:
            hi_draw = np.clip(hi, -13.5, 13.5)
            is_visible = X_MIN <= v <= X_MAX

            if is_visible:
                ax.annotate('', xy=(v, hi_draw), xytext=(v, 0), arrowprops=dict(arrowstyle="->", color='#2ca02c', lw=2.5))
                ax.text(v, hi_draw - 1.8 if hi_draw < 0 else hi_draw + 1.2, f'Image\n{hi:.1f}cm', color='#2ca02c', ha='center', fontsize=9, fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2ca02c", alpha=0.85))
                
                # Parallel Ray (reflects through F)
                ax.plot([u, 0], [ho, ho], color='orange', linestyle='--', lw=1.3)
                if v < 0:
                    ax.plot([0, v], [ho, hi_draw], color='orange', lw=1.3)
                else:
                    ax.plot([0, -25], [ho, ho + (ho - 0)/(0 - f)*(-25)], color='orange', lw=1.3)
                    ax.plot([0, v], [ho, hi_draw], color='orange', linestyle=':', lw=1.3)

                # Pole Ray (reflects at vertex)
                ax.plot([u, 0], [ho, 0], color='purple', linestyle='--', lw=1.3)
                if v < 0:
                    ax.plot([0, v], [0, hi_draw], color='purple', lw=1.3)
                else:
                    ax.plot([0, -25], [0, -(-ho/u)*(-25)], color='purple', lw=1.3)
                    ax.plot([0, v], [0, hi_draw], color='purple', linestyle=':', lw=1.3)
            else:
                # Out-of-bounds indicator for fixed optical bench
                target_edge = X_MAX if v > 0 else X_MIN
                ax.annotate(f'Image formed beyond bench\n(v = {v:.1f} cm, hi = {hi:.1f} cm)', 
                            xy=(target_edge - 2 if v > 0 else target_edge + 2, hi_draw), 
                            xytext=(target_edge - 28 if v > 0 else target_edge + 4, hi_draw),
                            arrowprops=dict(arrowstyle="->", color='#2ca02c', lw=2),
                            bbox=dict(boxstyle="round,pad=0.3", fc="#eafaf1", ec="#2ca02c", alpha=0.9),
                            fontsize=9, fontweight='bold', color='#2ca02c')
                ax.plot([u, 0], [ho, ho], color='orange', linestyle='--', lw=1.3)
                ax.plot([0, target_edge], [ho, ho + (hi - ho)/(v - 0)*(target_edge)], color='orange', lw=1.3)
                ax.plot([u, 0], [ho, 0], color='purple', linestyle='--', lw=1.3)
                ax.plot([0, target_edge], [0, (hi/v)*(target_edge)], color='purple', lw=1.3)

        # Enforce fixed axes styling
        ax.set_xlabel("Principal Axis (cm) — Optical Bench")
        ax.set_ylabel("Height (cm)")
        ax.grid(True, linestyle=':', alpha=0.5)
        st.pyplot(fig)


# =========================================================
# TAB 2: SPHERICAL LENS
# =========================================================
with tab_lens:
    st.header("Spherical Lens Simulation")
    col_l_ctrl, col_l_diag = st.columns([1, 2])
    
    with col_l_ctrl:
        l_type = st.selectbox("Lens Type:", ["Convex", "Concave"])
        u_mag_l = st.slider("Object Distance |u| (cm):", 5.0, 80.0, 35.0, 1.0, key="lens_u")
        f_mag_l = st.slider("Focal Length |f| (cm):", 10.0, 40.0, 20.0, 1.0, key="lens_f")
        ho_l = st.slider("Object Height (cm):", 1.0, 10.0, 4.0, 0.5, key="lens_ho")
        
        # Cartesian Sign Convention
        u_l = -u_mag_l
        f_l = f_mag_l if l_type == "Convex" else -f_mag_l
        
        denom_l = u_l + f_l
        at_focus_l = abs(denom_l) < 0.2
        
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

    with col_l_diag:
        fig2, ax2 = plt.subplots(figsize=(9, 4.8))
        
        # PERMANENTLY FIXED AXES & TICKS (Symmetric optical bench)
        X_MIN_L, X_MAX_L = -80.0, 80.0
        Y_MIN_L, Y_MAX_L = -15.0, 15.0
        ax2.set_xlim(X_MIN_L, X_MAX_L)
        ax2.set_ylim(Y_MIN_L, Y_MAX_L)
        ax2.set_xticks(np.arange(-80, 81, 20))
        ax2.set_yticks(np.arange(-15, 16, 5))
        ax2.set_autoscale_on(False)
        
        ax2.axhline(0, color='black', linewidth=1.2)
        
        # Fixed physical lens height
        LENS_HALF_HEIGHT = 10.0
        ax2.plot([0, 0], [-LENS_HALF_HEIGHT, LENS_HALF_HEIGHT], color='#1f77b4', linewidth=3)
        # Standard lens arrow tips
        tip = '^' if l_type == "Convex" else 'v'
        ax2.plot(0, LENS_HALF_HEIGHT, marker=tip, color='#1f77b4', markersize=9)
        ax2.plot(0, -LENS_HALF_HEIGHT, marker='v' if tip == '^' else '^', color='#1f77b4', markersize=9)

        # Mark Foci
        for pos, name in [(-f_mag_l, 'F1'), (f_mag_l, 'F2'), (-2*f_mag_l, '2F1'), (2*f_mag_l, '2F2')]:
            ax2.plot(pos, 0, 'ko', markersize=4)
            ax2.text(pos, -1.8, name, fontsize=10, ha='center',
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

        # Object Arrow
        ax2.annotate('', xy=(u_l, ho_l), xytext=(u_l, 0), arrowprops=dict(arrowstyle="->", color='#d62728', lw=2.5))
        ax2.text(u_l, ho_l + 1.2, f'Object\n{ho_l:.1f}cm', color='#d62728', ha='center', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#d62728", alpha=0.85))

        # Image Arrow and Rays
        if not at_focus_l:
            hi_draw_l = np.clip(hi_l, -13.5, 13.5)
            is_visible_l = X_MIN_L <= v_l <= X_MAX_L
            
            if is_visible_l:
                ax2.annotate('', xy=(v_l, hi_draw_l), xytext=(v_l, 0), arrowprops=dict(arrowstyle="->", color='#2ca02c', lw=2.5))
                ax2.text(v_l, hi_draw_l - 1.8 if hi_draw_l < 0 else hi_draw_l + 1.2, f'Image\n{hi_l:.1f}cm', color='#2ca02c', ha='center', fontsize=9, fontweight='bold',
                         bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2ca02c", alpha=0.85))
                
                # Parallel Ray
                ax2.plot([u_l, 0], [ho_l, ho_l], color='orange', linestyle='--', lw=1.3)
                if v_l > 0:
                    ax2.plot([0, v_l], [ho_l, hi_draw_l], color='orange', lw=1.3)
                else:
                    ax2.plot([0, 35], [ho_l, ho_l + (hi_draw_l - ho_l)/(v_l - 0)*(35)], color='orange', lw=1.3)
                    ax2.plot([0, v_l], [ho_l, hi_draw_l], color='orange', linestyle=':', lw=1.3)

                # Optical Center Ray
                ax2.plot([u_l, 0], [ho_l, 0], color='purple', linestyle='--', lw=1.3)
                if v_l > 0:
                    ax2.plot([0, v_l], [0, hi_draw_l], color='purple', lw=1.3)
                else:
                    ax2.plot([0, 35], [0, (hi_draw_l/v_l)*35], color='purple', lw=1.3)
                    ax2.plot([0, v_l], [0, hi_draw_l], color='purple', linestyle=':', lw=1.3)
            else:
                target_edge = X_MAX_L if v_l > 0 else X_MIN_L
                ax2.annotate(f'Image formed beyond bench\n(v = {v_l:.1f} cm, hi = {hi_l:.1f} cm)',
                             xy=(target_edge - 2 if v_l > 0 else target_edge + 2, hi_draw_l),
                             xytext=(target_edge - 28 if v_l > 0 else target_edge + 4, hi_draw_l),
                             arrowprops=dict(arrowstyle="->", color='#2ca02c', lw=2),
                             bbox=dict(boxstyle="round,pad=0.3", fc="#eafaf1", ec="#2ca02c", alpha=0.9),
                             fontsize=9, fontweight='bold', color='#2ca02c')
                ax2.plot([u_l, 0], [ho_l, ho_l], color='orange', linestyle='--', lw=1.3)
                ax2.plot([0, target_edge], [ho_l, ho_l + (hi_l - ho_l)/(v_l - 0)*(target_edge)], color='orange', lw=1.3)
                ax2.plot([u_l, 0], [ho_l, 0], color='purple', linestyle='--', lw=1.3)
                ax2.plot([0, target_edge], [0, (hi_l/v_l)*target_edge], color='purple', lw=1.3)

        # Enforce fixed axes styling
        ax2.set_xlabel("Principal Axis (cm) — Optical Bench")
        ax2.set_ylabel("Height (cm)")
        ax2.grid(True, linestyle=':', alpha=0.5)
        st.pyplot(fig2)


# =========================================================
# TAB 3: GLASS PRISM
# =========================================================
with tab_prism:
    st.header("Refraction Through Prism (NCERT Standard)")
    col_p_ctrl, col_p_diag = st.columns([1, 2])
    
    with col_p_ctrl:
        A = st.slider("Angle of Prism (A) in degrees:", 30.0, 75.0, 60.0, 1.0)
        n = st.slider("Refractive Index (n):", 1.20, 2.00, 1.50, 0.01)
        i = st.slider("Angle of Incidence (i) in degrees:", 20.0, 75.0, 45.0, 1.0)
        
        # Snell's Law calculations
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
            st.write(f"**Refraction angle 1 ($r_1$):** {r1:.2f}°")
            st.write(f"**Refraction angle 2 ($r_2$):** {r2:.2f}°")
            st.write(f"**Emergence angle ($e$):** {e:.2f}°")
            st.success(f"**Angle of Deviation ($\delta$):** {delta:.2f}°")
            st.info(f"**Minimum Deviation ($\delta_m$):** {delta_m:.2f}°")
        else:
            st.error(f"⚠️ Total Internal Reflection at Face 2 ($r_2 = {r2:.1f}^\circ > {critical_angle:.1f}^\circ$)")

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
        
        face_left_angle = math.atan2(apex[1] - left_base[1], apex[0] - left_base[0])
        face_right_angle = math.atan2(right_base[1] - apex[1], right_base[0] - apex[0])
        norm_left_angle = face_left_angle + math.pi / 2.0
        norm_right_angle = face_right_angle + math.pi / 2.0
        
        p_in = left_base + 0.5 * (apex - left_base)
        p_out = right_base + 0.5 * (apex - right_base)
        
        # Sideways incoming incident ray
        ray_len = 5.0
        inc_dir = norm_left_angle - math.pi + math.radians(i)
        p_start = p_in - ray_len * np.array([math.cos(inc_dir), math.sin(inc_dir)])
        
        # Draw Incident Ray
        ax3.plot([p_start[0], p_in[0]], [p_start[1], p_in[1]], color='red', lw=2.2)
        ax3.annotate('', xy=(p_in[0], p_in[1]), xytext=(p_start[0], p_start[1]),
                     arrowprops=dict(arrowstyle="-|>", color='red', lw=2))
        
        # Normal at Face 1
        n_len = 2.5
        norm_in_p1 = p_in + n_len * np.array([math.cos(norm_left_angle), math.sin(norm_left_angle)])
        norm_in_p2 = p_in - n_len * np.array([math.cos(norm_left_angle), math.sin(norm_left_angle)])
        ax3.plot([norm_in_p1[0], norm_in_p2[0]], [norm_in_p1[1], norm_in_p2[1]], 'k--', lw=1, alpha=0.6)

        # Refracted Ray inside prism
        ax3.plot([p_in[0], p_out[0]], [p_in[1], p_out[1]], color='orange', lw=2.2)

        # Normal at Face 2
        norm_out_p1 = p_out + n_len * np.array([math.cos(norm_right_angle), math.sin(norm_right_angle)])
        norm_out_p2 = p_out - n_len * np.array([math.cos(norm_right_angle), math.sin(norm_right_angle)])
        ax3.plot([norm_out_p1[0], norm_out_p2[0]], [norm_out_p1[1], norm_out_p2[1]], 'k--', lw=1, alpha=0.6)

        if not is_tir:
            em_dir = norm_right_angle - math.radians(e)
            p_end = p_out + ray_len * np.array([math.cos(em_dir), math.sin(em_dir)])
            
            # Emergent Ray pointing downwards toward base
            ax3.plot([p_out[0], p_end[0]], [p_out[1], p_end[1]], color='green', lw=2.2)
            ax3.annotate('', xy=(p_end[0], p_end[1]), xytext=(p_out[0], p_out[1]),
                         arrowprops=dict(arrowstyle="-|>", color='green', lw=2))
            
            # Forward & Backward Ray Extensions for Angle of Deviation
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
