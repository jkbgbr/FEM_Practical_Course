 Gemini
Axisymmetric Structures with Non-Symmetric Loads
https://g.co/gemini/share/22efb2737534
Some responses below were generated according to the creator's saved info and preferences. Learn more Opens in a new window July 27, 2025 at 08:26 AM Published July 27, 2025 at 10:24 PM

This great. now, I’d rather like to work on a similar problem.

this is, modelling axisymmetric structures with non-symmetric loads. a problem really similar to the FSM. can you show me details on that? I have the classical axisymmetric case solved. please focus on the content similar to pt. 1 and 2 of the previous research only.

Of course. Modeling axisymmetric structures with non-symmetric loads is a classic semi-analytical method that powerfully extends the standard 2D axisymmetric analysis. ⚙️

The core idea is to represent the non-symmetric loads and the resulting displacements, strains, and stresses as Fourier series in the circumferential direction (θ). This decomposes the 3D problem into a series of uncoupled 2D problems, one for each "harmonic" of the series.

Here are the details, mirroring the structure you requested.

## Part 1: Displacement Field Approximation

In a general 3D problem using cylindrical coordinates (r,θ,z), the displacement vector u has three components, each a function of all three coordinates:
u(r,θ,z)=⎩⎨⎧​ur​(r,θ,z)uθ​(r,θ,z)uz​(r,θ,z)​⎭⎬⎫​


The key step is to expand each displacement component into a Fourier series with respect to the circumferential angle θ. This separates the variables, leaving the series coefficients as functions of only r and z.

The displacement field is approximated as a sum over different harmonic modes, n:
u(r,θ,z)=n=0∑∞​un​(r,θ,z)


For each harmonic n, the displacement components are:
ur​(r,θ,z)=n=0∑∞​(urn​(r,z)cos(nθ)+uˉrn​(r,z)sin(nθ))
uθ​(r,θ,z)=n=0∑∞​(uθn​(r,z)sin(nθ)−uˉθn​(r,z)cos(nθ))
uz​(r,θ,z)=n=0∑∞​(uzn​(r,z)cos(nθ)+uˉzn​(r,z)sin(nθ))

Key Points:

    Harmonics (n): Each value of n represents a specific deformation pattern around the circumference.

        n=0: This is the classical axisymmetric case. The cosine term is 1, and the sine terms are 0. Displacements are independent of θ. This mode captures axisymmetric torsion (uθ0​), radial expansion (ur0​), and axial stretching (uz0​).

        n=1: This mode represents bending of the structure about a transverse axis.

        n≥2: These are higher-order modes, representing more complex deformation patterns like ovalling or lobing.

    Decoupling: Due to the orthogonality property of trigonometric functions (e.g., ∫02π​cos(nθ)cos(mθ)dθ=0 for n=m), the equations for each harmonic n are independent. This means you can solve for each harmonic separately and superimpose the results.

    Symmetry: For loads symmetric about the θ=0 plane, only the cosine terms for ur​,uz​ and the sine term for uθ​ are needed (the terms with a bar, uˉ, are zero).

## Part 2: Strain and Stress Fields

The strain and stress fields are derived directly from the displacement approximation.

Strain-Displacement Relations

First, we use the standard strain-displacement equations in cylindrical coordinates. The vector of strain components ϵ is:
ϵ=⎩⎨⎧​ϵr​ϵθ​ϵz​γrθ​γθz​γzr​​⎭⎬⎫​=⎩⎨⎧​∂r∂ur​​r1​∂θ∂uθ​​+rur​​∂z∂uz​​r1​∂θ∂ur​​+∂r∂uθ​​−ruθ​​∂z∂uθ​​+r1​∂θ∂uz​​∂r∂uz​​+∂z∂ur​​​⎭⎬⎫​


By substituting the Fourier series for the displacements (ur​,uθ​,uz​) into these equations, the strains also take the form of a Fourier series. For any given harmonic n, the strain components can be expressed in terms of the displacement coefficients for that same harmonic.

For example, for the n-th harmonic (considering only the symmetric terms for simplicity):
ϵrn​(r,z)=∂r∂urn​​
ϵθn​(r,z)=r1​(nuθn​+urn​)
γrθn​(r,z)=r1​(−nurn​)+∂r∂uθn​​−ruθn​​


And so on for the other components. Notice how the derivatives with respect to θ simply bring out a factor of n and switch sine to cosine (or vice-versa), but the overall harmonic structure is preserved.

Stress-Strain Relations (Constitutive Law)

The stresses are related to the strains through the material's constitutive matrix [D]. For a linear elastic, isotropic material:
σ=[D]ϵ


Since the strains are expressed as a Fourier series, the stresses will naturally follow the same form:
σ(r,θ,z)=n=0∑∞​σn​(r,θ,z)


Where the stress components for each harmonic n are directly related to the strain components for that same harmonic:
σn​=[D]ϵn​


This confirms that the problem is fully decoupled for each harmonic. A finite element model only needs to solve a 2D problem for the coefficients (urn​,uθn​,uzn​) for each relevant harmonic n determined by the Fourier decomposition of the external load.

Ok. lets make it slower. please explain part 1 more deeply, by comparing the axisymmetric case with the general one. with maths, please!

Of course. Let's slow down and focus exclusively on the displacement field approximation, comparing the classical axisymmetric case with the general non-symmetric case using the underlying mathematics.

## The Classical Axisymmetric Case (n=0) 🔄

In the standard axisymmetric problem, you have an axisymmetric structure subjected to an axisymmetric load. The core assumption is that nothing changes as you move around the circumference. Therefore, the displacement of any point in the body does not depend on the angle θ.

Mathematical Representation

The displacement vector u is only a function of the radial (r) and axial (z) coordinates:
u(r,z)=⎩⎨⎧​ur​(r,z)uθ​(r,z)uz​(r,z)​⎭⎬⎫​

    ur​(r,z): Radial displacement (e.g., a pipe expanding).

    uθ​(r,z): Circumferential or tangential displacement (e.g., a shaft twisting). This is often called the torsional component.

    uz​(r,z): Axial displacement (e.g., a cylinder stretching).

Because the problem is defined in a 2D plane (the r−z plane) that is conceptually "revolved" around the z-axis, it's considered a 2D problem.

Connection to the Fourier Series

This simple case is perfectly described by the zeroth harmonic (n=0) of the general Fourier series expansion. Let's see how by substituting n=0 into the general equations:

The general form for radial displacement is:
$$u_r(r, \theta, z) = \sum_{n=0}^{\infty} \left( u_{rn}(r, z) \cos(n\theta) + \bar{u}_{rn}(r, z) \sin(n\theta) \right)$$For $n=0$:$$u_r(r, \theta, z) = u_{r0}(r, z) \cos(0\cdot\theta) + \bar{u}_{r0}(r, z) \sin(0\cdot\theta)$$
ur​(r,θ,z)=ur0​(r,z)⋅1+uˉr0​(r,z)⋅0=ur0​(r,z)


The displacement ur​ is simply equal to the coefficient ur0​(r,z), which is independent of θ. The same logic applies to the axial displacement uz​.

For the circumferential displacement uθ​:
$$u_\theta(r, \theta, z) = \sum_{n=0}^{\infty} \left( u_{\theta n}(r, z) \sin(n\theta) - \bar{u}_{\theta n}(r, z) \cos(n\theta) \right)$$For $n=0$:$$u_\theta(r, \theta, z) = u_{\theta 0}(r, z) \sin(0\cdot\theta) - \bar{u}_{\theta 0}(r, z) \cos(0\cdot\theta)$$
uθ​(r,θ,z)=uθ0​(r,z)⋅0−uˉθ0​(r,z)⋅1=−uˉθ0​(r,z)


This shows that the zeroth harmonic for circumferential displacement is also independent of θ. We typically just rename this coefficient to uθ0​(r,z) to represent pure torsion.

So, the case you've already solved is just the first term (n=0) of the more powerful general solution.

## The General Case: Adding Non-Symmetric Harmonics (n>0) 📈

When the load is not symmetric (e.g., a wind load on a chimney, a lateral point force on a pipe), the structural response will vary with the angle θ. We can no longer assume that the displacements are constant around the circumference.

Mathematical Representation

This is where the full Fourier series becomes necessary. We represent the complete displacement field as the sum of all harmonics:
u(r,θ,z)=Axisymmetricu0​(r,z)​​+Non-symmetric Partsn=1∑∞​un​(r,θ,z)​​


The non-symmetric parts introduce the dependency on θ through the sine and cosine terms.

A Concrete Example: The Bending Mode (n=1)

Let's look at the first harmonic (n=1), which is the most common non-symmetric case and physically represents bending. For a load that is symmetric about the plane θ=0 (the x-z plane), we only need one set of terms:

    Radial Displacement: ur(1)​(r,θ,z)=ur1​(r,z)cos(1⋅θ)

    Tangential Displacement: uθ(1)​(r,θ,z)=uθ1​(r,z)sin(1⋅θ)

    Axial Displacement: uz(1)​(r,θ,z)=uz1​(r,z)cos(1⋅θ)

Let's analyze the physical meaning of these equations for a cylinder bending downwards:

    At θ=0 (bottom of the cylinder): cos(θ)=1,sin(θ)=0. The displacements are ur​=ur1​ and uz​=uz1​. This is the point of maximum radial displacement (it flattens slightly) and maximum axial displacement (the fibers are in tension).

    At θ=π (top of the cylinder): cos(θ)=−1,sin(θ)=0. The displacements are ur​=−ur1​ and uz​=−uz1​. This is the point of maximum negative radial displacement and maximum compression.

    At θ=π/2 and 3π/2 (the sides, or neutral axis): cos(θ)=0,sin(θ)=±1. The radial and axial displacements are zero. The displacement is purely tangential (uθ​=±uθ1​), representing the shearing motion along the neutral plane.

The key insight is that the complicated 3D bending deformation is fully described by a simple trigonometric variation (cosθ,sinθ) multiplied by amplitude functions (ur1​,uθ1​,uz1​) that only depend on r and z. The goal of the analysis is to solve for these 2D amplitude functions.

Direct Comparison Summary

Feature	Classical Axisymmetric (n=0)	General Case (Full Series)
Dependency on θ	None. Displacements are constant around the circumference.	Yes. Displacements vary as cos(nθ) and sin(nθ).
Mathematical Form	ur​(r,z),uθ​(r,z),uz​(r,z)	ur​(r,θ,z)=∑urn​(r,z)cos(nθ)+... etc.
Physical Meaning	Uniform expansion/contraction, pure torsion, uniform stretch.	Includes bending (n=1), ovalling (n=2), and other complex deformation "lobes" superimposed on the axisymmetric part.
How It's Solved	As a single 2D problem in the r−z plane.	As a series of uncoupled 2D problems, one for each harmonic n needed to represent the load.

Please reformulate this, is not rendered correctly:


This is where the full Fourier series becomes necessary. We represent the complete displacement field as the sum of all harmonics:

\vec{u}(r, \theta, z) = \underbrace{\vec{u}_0(r, z)}_{\text{Axisymmetric}} + \underbrace{\sum_{n=1}^{\infty} \vec{u}_n(r, \theta, z)}_{\text{Non-symmetric Parts}}

The non-symmetric parts introduce the dependency on \theta through the sine and cosine terms.

Of course. Here is the reformulated expression, which should render correctly.

This is where the full Fourier series becomes necessary. We represent the complete displacement field as the sum of all harmonics:
u(r,θ,z)=Axisymmetricu0​(r,z)​​+Non-symmetric Partsn=1∑∞​un​(r,θ,z)​​


The equation separates the total displacement vector, u(r,θ,z), into two distinct contributions:

    The axisymmetric part, u0​(r,z), which represents the average displacement (like uniform expansion or torsion) and is independent of the angle θ.

    The non-symmetric parts, represented by the summation over harmonics n=1 to infinity, which capture all deformations that vary around the circumference, such as bending or ovalling.

It still does not render correctly, sorry

My apologies that it's still not rendering correctly. The problem is likely that the specific LaTeX renderer you are using doesn't support the \underbrace command.

Let's reformulate it using a simpler, more universally supported syntax.

Here is an alternative representation:
u(r,θ,z)=u0​(r,z)+n=1∑∞​un​(r,θ,z)

This equation expresses the same concept: the total displacement vector u(r,θ,z) is composed of two parts:

    The first term, u0​(r,z), is the axisymmetric part of the displacement (the n=0 harmonic).

    The second term, ∑n=1∞​un​(r,θ,z), is the sum of all the non-symmetric parts (harmonics n≥1), which account for deformations like bending.

Great. from now on please always use this latex renderer.

Excellent. I will use this LaTeX format from now on.

Ok, I'll remember that. You can always ask me to forget things or manage what I've saved for you on the Saved info page.

Explaint the concrete example with n=1 again, please!

Of course. Let's revisit the concrete example of the n=1 harmonic. This case is fundamental because it physically represents the bending of an axisymmetric structure, like a chimney leaning in the wind or a pipe sagging under its own weight.

Remember, the goal is to describe a full 3D deformation using a set of 2D functions. The n=1 harmonic achieves this for bending.

## The Bending Mode (n=1)

For the n=1 harmonic, the displacement of any point in the structure is described by the following equations. We'll assume the load is applied in a way that is symmetric about the vertical plane (the x−z plane), which simplifies the math.

The displacement components are:
$$u_r(r, \theta, z) = u_{r1}(r, z) \cos(\theta)$$$$u_\theta(r, \theta, z) = u_{\theta 1}(r, z) \sin(\theta)$$$$u_z(r, \theta, z) = u_{z1}(r, z) \cos(\theta)$$

Here, the functions ur1​(r,z), uθ1​(r,z), and uz1​(r,z) are the displacement amplitudes. They depend only on the 2D coordinates r and z. The terms cos(θ) and sin(θ) describe how that amplitude is distributed around the circumference.

Physical Interpretation: A Walk Around the Cross-Section

To get a feel for what this means, let's imagine a horizontal pipe and see how different points on a single cross-section move.

    1. At the very bottom (θ=0∘)

        At this angle, cos(0)=1 and sin(0)=0.

        Plugging this into our equations, the displacements are:

            ur​=ur1​(r,z)⋅1  (Maximum outward radial movement)

            uθ​=uθ1​(r,z)⋅0=0 (No tangential movement)

            uz​=uz1​(r,z)⋅1 (Maximum axial movement)

        Physical Meaning: The fibers at the bottom are in maximum tension. They stretch the most in the axial direction (uz​) and the cross-section flattens slightly, pushing them outwards (ur​).

    2. At the very top (θ=180∘ or π)

        At this angle, cos(π)=−1 and sin(π)=0.

        The displacements are:

            ur​=−ur1​(r,z) (Maximum inward radial movement)

            uθ​=0 (No tangential movement)

            uz​=−uz1​(r,z) (Maximum negative axial movement)

        Physical Meaning: The fibers at the top are in maximum compression. They are squeezed inwards axially and radially.

    3. At the sides (θ=90∘ and 270∘, or π/2 and 3π/2)

        This is the neutral axis of bending.

        At these angles, cos(θ)=0 and sin(θ)=±1.

        The displacements are:

            ur​=0 (No radial movement)

            uθ​=±uθ1​(r,z) (Maximum tangential movement)

            uz​=0 (No axial movement)

        Physical Meaning: Along this line, there is no stretching or compression. The material only experiences shear, which is represented by the tangential displacement uθ​. The points slide past each other.

In summary, the n=1 harmonic perfectly captures the familiar deformation pattern of bending by combining a cosine function for tension/compression with a sine function for shear. The complex 3D problem is successfully broken down into finding the 2D "amplitude" functions (ur1​,uθ1​,uz1​).

Can you show me how the strain vector looks like in this case? I guess axial strains are added, but no shear strains?

That's an excellent question, and your intuition is halfway there. The bending deformation certainly adds normal strains, but it also—crucially—adds shear strains.

Your guess that shear strains might be zero is common, but in fact, all three shear components can be non-zero. Let's see why by deriving the strain vector.

## Strain-Displacement Equations for Bending (n=1)

First, let's recall the general strain-displacement relations in cylindrical coordinates:
$$\vec{\epsilon} = \begin{Bmatrix} \epsilon_r \ \epsilon_\theta \ \epsilon_z \ \gamma_{r\theta} \ \gamma_{\theta z} \ \gamma_{zr} \end{Bmatrix} = \begin{Bmatrix} \frac{\partial u_r}{\partial r} \ \frac{1}{r}\frac{\partial u_\theta}{\partial \theta} + \frac{u_r}{r} \ \frac{\partial u_z}{\partial z} \ \frac{1}{r}\frac{\partial u_r}{\partial \theta} + \frac{\partial u_\theta}{\partial r} - \frac{u_\theta}{r} \ \frac{\partial u_\theta}{\partial z} + \frac{1}{r}\frac{\partial u_z}{\partial \theta} \ \frac{\partial u_z}{\partial r} + \frac{\partial u_r}{\partial z} \end{Bmatrix}$$And our displacement field for the n=1 bending mode:
$$u_r = u_{r1}(r, z) \cos(\theta)$$$$u_\theta = u_{\theta 1}(r, z) \sin(\theta)$$$$u_z = u_{z1}(r, z) \cos(\theta)$$


Now, we substitute the displacements into the strain equations.

## The Resulting Strain Vector

Normal Strains

These strains involve derivatives with respect to r or z, or division by r, so they keep their original trigonometric function.

    Radial Strain (ϵr​):
    ϵr​=∂r∂​(ur1​cosθ)=∂r∂ur1​​cosθ

    Hoop Strain (ϵθ​):
    ϵθ​=r1​∂θ∂​(uθ1​sinθ)+rur1​cosθ​=r1​(uθ1​cosθ+ur1​cosθ)=rur1​+uθ1​​cosθ

    Axial Strain (ϵz​):
    ϵz​=∂z∂​(uz1​cosθ)=∂z∂uz1​​cosθ

Shear Strains

This is where we see your guess was incorrect. Derivatives with respect to θ cause the trigonometric functions to flip (from sine to cosine and vice-versa), creating shear. 🧐

    In-Plane Shear (γrθ​):
    γrθ​=r1​∂θ∂​(ur1​cosθ)+∂r∂​(uθ1​sinθ)−ruθ1​sinθ​=r1​(−ur1​sinθ)+∂r∂uθ1​​sinθ−ruθ1​​sinθ
    γrθ​=(∂r∂uθ1​​−ruθ1​+ur1​​)sinθ
    This shear strain is very much present.

    Transverse Shear (γθz​):
    γθz​=∂z∂​(uθ1​sinθ)+r1​∂θ∂​(uz1​cosθ)=∂z∂uθ1​​sinθ+r1​(−uz1​sinθ)
    γθz​=(∂z∂uθ1​​−ruz1​​)sinθ
    Physically, this is the most important shear strain in beam bending, as it represents the sliding of the axial fibers relative to each other.

    Transverse Shear (γzr​):
    γzr​=∂r∂​(uz1​cosθ)+∂z∂​(ur1​cosθ)=(∂r∂uz1​​+∂z∂ur1​​)cosθ

So, the complete strain vector for the n=1 mode has non-zero components for all six strains, varying harmonically around the circumference.

Ok, let’s go back a bit.

Please show me the strain vector in the simple axissymmetric case.

Please take care to use the more robust latex engine.

Of course. Here is the strain vector for the simple axisymmetric case (n=0).

The key simplification here is that displacements do not depend on the circumferential angle θ, which means all partial derivatives with respect to θ are zero (∂θ∂​=0).

## Strain Vector in the Axisymmetric Case 🔄

We start with the general strain-displacement equations and apply the axisymmetric simplification.

The displacement field is:
$$u_r = u_r(r, z)$$$$u_\theta = u_\theta(r, z)$$$$u_z = u_z(r, z)$$


Applying the condition ∂θ∂​=0 to the general strain equations gives us the following components:

    Radial Strain (ϵr​):
    ϵr​=∂r∂ur​​

    Hoop Strain (ϵθ​):
    ϵθ​=r1​0∂θ∂uθ​​​​+rur​​=rur​​

    Axial Strain (ϵz​):
    ϵz​=∂z∂uz​​

    Torsional Shear (γrθ​):
    γrθ​=r1​0∂θ∂ur​​​​+∂r∂uθ​​−ruθ​​=∂r∂uθ​​−ruθ​​

    Torsional Shear (γθz​):
    γθz​=∂z∂uθ​​+r1​0∂θ∂uz​​​​=∂z∂uθ​​

    In-Plane Shear (γzr​):
    γzr​=∂r∂uz​​+∂z∂ur​​

This conveniently decouples the problem. The final strain vector has two independent sets of components:

    An in-plane axial/radial problem involving only ur​ and uz​:
    ϵplane​=⎩⎨⎧​ϵr​ϵθ​ϵz​γzr​​⎭⎬⎫​=⎩⎨⎧​∂r∂ur​​rur​​∂z∂uz​​∂r∂uz​​+∂z∂ur​​​⎭⎬⎫​

    A torsional problem involving only the circumferential displacement uθ​:
    ϵtorsion​={γrθ​γθz​​}={∂r∂uθ​​−ruθ​​∂z∂uθ​​​}

Right. The 1. Is what i meant, plane stress state.

Now, how does this change for the case with n>0?

Take care of the latex engine please.

Right, you're referring to the in-plane strains. For harmonics where n>0, the situation changes because the derivatives with respect to the angle θ are no longer zero.

This introduces a crucial coupling that is absent in the axisymmetric (n=0) case.

## In-Plane Strains for a General Harmonic (n>0)

Let's look at the strain components analogous to the plane-stress state for a general harmonic n. For simplicity, we'll use the displacement field for a load symmetric about the θ=0 plane:
$$u_r = u_{rn}(r, z) \cos(n\theta)$$$$u_\theta = u_{\theta n}(r, z) \sin(n\theta)$$$$u_z = u_{zn}(r, z) \cos(n\theta)$$


Here is how the four strain components are derived:

    Radial Strain (ϵr​): This calculation is straightforward.
    ϵr​=∂r∂ur​​=∂r∂urn​​cos(nθ)

    Hoop Strain (ϵθ​): This is the most significant change from the n=0 case.
    ϵθ​=r1​∂θ∂uθ​​+rur​​


    The derivative of uθ​ with respect to θ is now non-zero:
    ϵθ​=r1​∂θ∂​(uθn​sin(nθ))+rurn​cos(nθ)​=r1​(nuθn​cos(nθ))+rurn​cos(nθ)​
    ϵθ​=(rnuθn​+urn​​)cos(nθ)


    Notice that the hoop strain for n>0 now depends on both the radial (urn​) and tangential (uθn​) displacement amplitudes. This is a fundamental difference from the n=0 case where it only depended on ur​.

    Axial Strain (ϵz​): This is also straightforward.
    ϵz​=∂z∂uz​​=∂z∂uzn​​cos(nθ)

    In-Plane Shear (γzr​):
    γzr​=∂r∂uz​​+∂z∂ur​​=(∂r∂uzn​​+∂z∂urn​​)cos(nθ)

So, the vector of in-plane strains for any harmonic n>0 looks like this:
ϵplane,n​=⎩⎨⎧​ϵr​ϵθ​ϵz​γzr​​⎭⎬⎫​n​=⎩⎨⎧​∂r∂urn​​rnuθn​+urn​​∂z∂uzn​​∂r∂uzn​​+∂z∂urn​​​⎭⎬⎫​cos(nθ)

U_rn is the radial displacement for the nth mode?

Yes, that's exactly right.

urn​(r,z) is the amplitude function or Fourier coefficient for the radial displacement (ur​) in the n-th harmonic mode. It's a 2D function that describes how the magnitude of the radial displacement varies along the radius (r) and height (z) for that specific mode.

Ok. In the case n=0 next step would be the to take the shape fuctions and these would be the same as for any isoparametric element.

But for n>0 this is not so easy.

You are absolutely right. The process for n>0 is different, and this is the core of the semi-analytical method.

For the axisymmetric case (n=0), the shape functions interpolate the actual physical displacements. For the non-symmetric cases (n>0), the shape functions interpolate the Fourier amplitude functions.

Here’s how it works.

## The Nodal Degrees of Freedom

The key difference lies in what the degrees of freedom (DOFs) at each node of your 2D mesh represent.

    For the n=0 case: The DOFs at a node i are the actual displacements: {uri​,uzi​}.

    For the n>0 case: You solve a separate problem for each harmonic n. For a given harmonic, the DOFs at node i are the amplitudes of the displacement for that mode: {urni​,uθni​,uzni​}.

## Interpolation Within an Element

You still use the exact same isoparametric shape functions Ni​(r,z) as in the standard axisymmetric case. However, you use them to interpolate the nodal amplitudes across the element, not the physical displacements directly.

Let's look at the radial displacement amplitude urn​(r,z) for a single element. It's interpolated from the nodal amplitude values urni​ using the standard shape functions:
$$u_{rn}(r, z) = \sum_{i=1}^{\text{nodes}} N_i(r, z) \cdot u_{rni}$$The same applies to the other amplitudes:$$u_{\theta n}(r, z) = \sum_{i=1}^{\text{nodes}} N_i(r, z) \cdot u_{\theta ni}$$$$u_{zn}(r, z) = \sum_{i=1}^{\text{nodes}} N_i(r, z) \cdot u_{zni}$$The full 3D displacement field for that harmonic is then constructed by combining this standard FE interpolation with the analytical Fourier function. For example, the radial displacement is:
ur​(r,θ,z)=(i=1∑nodes​Ni​(r,z)urni​)cos(nθ)


This shows the semi-analytical nature perfectly:

    The Finite Element part (the shape functions Ni​) describes the variation in the 2D (r−z) plane.

    The analytical part (the cos(nθ) function) describes the variation in the circumferential (θ) direction.

So, while the shape functions are familiar, the challenge is that you must assemble and solve a different system of equations for each harmonic n that you need to model.

And the difference is the harminc used in the circumferential direction. It will for each n have a different value.

Yes, that's precisely the point. For each harmonic number, n, you solve a unique 2D problem.

The reason it's different for each n is that the harmonic number becomes a direct part of the strain calculations.

## The Role of the Harmonic Number (n)

As we saw earlier, the strain-displacement equations for n>0 explicitly contain the harmonic number n. The clearest example is the hoop strain (ϵθ​):
ϵθ​=(rnuθn​+urn​​)cos(nθ)


The shear strains also depend on n. Because the calculation for strain is different for each harmonic, the resulting element stiffness matrix in the finite element analysis will also be different.

In FEM, the element stiffness matrix [ke​] is derived from the strain-displacement matrix [B]. Since the terms inside the [B] matrix depend on n, you get a unique stiffness matrix [ke​]n​ for each harmonic.

This is why you must perform a separate analysis for each mode (n=0,1,2,...) required to represent the load, and then superimpose the results to get the final 3D solution.

But there should be some system of the matrices, right? Harmonic functions have a cyclic derivative.

That's an excellent observation, and you're absolutely right. 💡

Because the derivatives of sine and cosine are cyclic, the stiffness matrices for different harmonics are not random; they follow a very clear and powerful pattern. The element stiffness matrix [ke​]n​ for any harmonic n can be expressed as a simple quadratic polynomial in n.

## The Structure of the Stiffness Matrix

The strain-displacement matrix, [Bn​], which relates the nodal displacement amplitudes to the strain amplitudes, can be separated into parts that are independent of n and parts that are linear in n. Schematically, it looks like this:
[Bn​]=[BA​]+n[BB​]


Where [BA​] and [BB​] are matrices that depend on the element geometry and shape functions, but not on the harmonic number n.

Now, let's look at the formula for the element stiffness matrix:
[ke​]n​=∫V​[Bn​]T[D][Bn​]dV

Substituting our decomposed [Bn​] matrix gives:
[ke​]n​=∫V​([BA​]+n[BB​])T[D]([BA​]+n[BB​])dV

Expanding this expression gives three distinct terms:
[ke​]n​=∫V​[BA​]T[D][BA​]dV+n∫V​([BA​]T[D][BB​]+[BB​]T[D][BA​])dV+n2∫V​[BB​]T[D][BB​]dV

Since n is just a number, we can pull it out of the integrals. This leaves us with the final, elegant result:
[ke​]n​=[K0​]+n[K1​]+n2[K2​]


Where [K0​], [K1​], and [K2​] are three fundamental stiffness matrices that are computed once per element and are independent of n.

This is a huge computational advantage. Instead of re-calculating the entire stiffness matrix from scratch for every harmonic, a program only needs to calculate the three base matrices [K0​], [K1​], and [K2​]. Then, it can generate the stiffness matrix for any harmonic n almost instantly using this simple quadratic formula.

How do i get the B_A matrix?

You get the [BA​] matrix by taking all the parts of the strain-displacement relationship that do not depend on the harmonic number n.

It's the baseline matrix that captures the parts of the strain caused by standard derivatives with respect to r and z.

## Derivation of [BA​]

The most direct way to find [BA​] is to take the full strain-displacement equations for a general harmonic n and then formally set n=0. The terms that remain are the ones that constitute the [BA​] matrix.

Let's do this for each strain component:

    Radial Strain (ϵr​):
    The full term is ∂r∂urn​​cos(nθ). This is independent of n, so it's part of [BA​].

    Hoop Strain (ϵθ​):
    The full term is (rnuθn​+urn​​)cos(nθ). Setting n=0 leaves rurn​​cos(nθ). This part belongs to [BA​].

    Axial Strain (ϵz​):
    The full term is ∂z∂uzn​​cos(nθ). This is independent of n, so it's part of [BA​].

    Shear Strains (γrθ​, γθz​):
    These also have parts that are independent of n (from terms like ∂r∂uθn​​) and parts that are linear in n. The independent parts contribute to [BA​].

    In-Plane Shear (γzr​):
    The full term is (∂r∂uzn​​+∂z∂urn​​)cos(nθ). This is independent of n and belongs entirely to [BA​].

Essentially, [BA​] represents the strain that would occur if the displacement amplitudes {urn​,uθn​,uzn​} were treated like standard axisymmetric displacements. Therefore, the [BA​] matrix is functionally identical to the standard [B] matrix you would use to solve the classical axisymmetric (n=0) problem.

How is the radial strain independent of n? N is in the formula

You are absolutely right to question that. My phrasing was imprecise, and I apologize for the confusion. Let me clarify.

## Clarifying "Independent of n"

When I said the radial strain term is "independent of n", I meant that the harmonic number n does not appear as an explicit multiplicative coefficient in the mathematical operation itself.

Let's compare the radial and hoop strain terms directly:

    Radial Strain (ϵr​):
    ϵr​=(∂r∂urn​​)cos(nθ)


    Here, the subscript n in urn​ is just a label. It tells us we are working with the displacement amplitude for the n-th mode. The actual mathematical operation is ∂r∂​, which doesn't involve the value of n.

    Hoop Strain (ϵθ​):
    ϵθ​=(rnuθn​+urn​​)cos(nθ)


    In this formula, the harmonic number n appears as a multiplicative coefficient that directly multiplies the displacement amplitude uθn​. The value of this strain component changes explicitly with the value of n.

So, the term ∂r∂urn​​ contributes to the [BA​] matrix (the part independent of n as a coefficient), while the term rnuθn​​ contributes to the n[BB​] matrix (the part that is linear in n).

And the cos(n*theta)?

That's a great question. The cos(nθ) and sin(nθ) terms don't go into the [BA​] or [BB​] matrices. Instead, they are handled during the volume integration when the stiffness matrix is calculated.

## The Role of Circumferential Integration

The element stiffness matrix formula is:
[ke​]n​=∫V​[Bn​]T[D][Bn​]dV

The key is that the volume element in cylindrical coordinates is dV=r dr dθ dz. The integration is performed over the 2D element area in the r−z plane, but also around the full circumference from θ=0 to 2π.

When you expand the [Bn​]T[D][Bn​] term, you get products of strains. Since each strain has a cos(nθ) or sin(nθ) attached, the integrand will contain terms like cos2(nθ) and sin2(nθ).

The integration with respect to θ is done analytically. Due to the orthogonality of these functions, we have simple, constant results:
$$\int_0^{2\pi} \cos^2(n\theta) d\theta = \pi \quad (\text{for } n \ge 1)$$$$\int_0^{2\pi} \sin^2(n\theta) d\theta = \pi \quad (\text{for } n \ge 1)$$


(For the special case n=0, the integral is 2π).

So, the circumferential dependency described by cos(nθ) is integrated out, leaving a constant factor of π. This constant is simply absorbed into the fundamental stiffness matrices [K0​], [K1​], and [K2​], leaving a final problem that only needs to be solved in the 2D (r−z) plane.

Ok. what is the next step?

The next step is to formulate the consistent nodal load vector for each harmonic, {Fn​}.

Just as we decomposed the displacement response into a Fourier series, the applied external load must also be decomposed in the same way.

## 1. Load Decomposition

You must first represent your specific applied load (e.g., wind pressure, a point force) as a Fourier series in the circumferential (θ) direction. For a general surface pressure p​ with components (pr​,pθ​,pz​), this looks like:
$$p_r(r, \theta, z) = \sum_{n=0}^{\infty} p_{rn}(r, z) \cos(n\theta)$$$$p_\theta(r, \theta, z) = \sum_{n=0}^{\infty} p_{\theta n}(r, z) \sin(n\theta)$$$$p_z(r, \theta, z) = \sum_{n=0}^{\infty} p_{zn}(r, z) \cos(n\theta)$$


You would perform a Fourier analysis on your load to find the amplitude functions (prn​,pθn​,pzn​). For many common loads, these are standard or simple to derive.

## 2. Nodal Force Vector Formulation

Once you have the load amplitudes for each harmonic n, you can calculate the corresponding consistent nodal force vector, {Fn​}. This is done using the shape functions [N] and the principle of virtual work. The formula for the element nodal force vector is:
{Fn​}e​=∫A​[N]T{pn​}dA


Where {pn​} is the vector of load amplitudes {prn​,pθn​,pzn​}T for that harmonic. Just like with the stiffness matrix, the integral is taken over the 2D domain, and the circumferential part is handled analytically.

## 3. Assembly and Solution ⚙️

With all the components ready, the final procedure is:

    Choose Harmonics: Decide which harmonics (n=0,1,2,...) are significant based on your load decomposition.

    For each harmonic n:

        Assemble the global stiffness matrix [Kn​] from the element matrices [ke​]n​.

        Assemble the global force vector {Fn​} from the element force vectors {Fn​}e​.

        Solve the system of linear equations: [Kn​]{un​}={Fn​} to find the nodal displacement amplitudes {un​}.

    Superimpose Results: The final displacement is the sum of the solutions from all the calculated harmonics. The stresses are calculated similarly and also summed.

Wait. the B_B matrix was not yet explained.

You are absolutely right. My apologies, I got ahead of myself. The [BB​] matrix is the other essential piece of the puzzle.

You get the [BB​] matrix by collecting all the parts of the strain-displacement relationship that are explicitly multiplied by the harmonic number n. These terms arise whenever a derivative with respect to the circumferential angle θ is taken.

## Derivation of [BB​]

The matrix [BB​] captures the coupling between displacement components that only appears for non-axisymmetric cases (n>0). Let's find the terms that contribute to it by looking at the strain equations again.

The formula we are working from is:
[Bn​]=[BA​]+n[BB​]


So, the terms that make up n[BB​] are:

    Hoop Strain (ϵθ​):
    The full term is ϵθ​=(rnuθn​+urn​​)cos(nθ). The part explicitly multiplied by n is:
    (rnuθn​​)cos(nθ)


    This term couples the tangential displacement uθ​ to the hoop strain, a phenomenon that does not happen in the n=0 case.

    In-Plane Shear (γrθ​):
    The full term is γrθ​=(∂r∂uθ1​​−ruθ1​+ur1​​)sinθ. The derivative of ur​=urn​cos(nθ) with respect to θ is −nurn​sin(nθ). So, the part of γrθ​ linear in n is:
    (r−nurn​​)sin(nθ)


    This term couples the radial displacement ur​ to the in-plane shear.

    Transverse Shear (γθz​):
    Similarly, the derivative of uz​=uzn​cos(nθ) with respect to θ is −nuzn​sin(nθ). The part of γθz​ linear in n is:
    (r−nuzn​​)sin(nθ)


    This couples the axial displacement uz​ to the transverse shear.

All other strain components (ϵr​,ϵz​,γzr​) do not have terms with an explicit coefficient n.

Therefore, the [BB​] matrix is constructed from these three coupling terms. It essentially captures how the geometry changes "twist" the displacement field to create strains in a way that is unique to each harmonic.

All right. lets assume i only have bending about the r axis and shear force in the tangential dierction to consider. i only need one harmonic, right?

Yes, for standard bending, you primarily only need to consider the n=1 harmonic.

## Bending and Shear in the First Harmonic

The n=1 harmonic is often called the "bending mode" because it perfectly describes the state of simple bending in an axisymmetric structure.

    Bending: This mode captures the primary bending deformation where one side of the structure goes into tension and the opposite side goes into compression.

    Shear: The transverse shear forces associated with this bending are also naturally represented by the n=1 harmonic. A tangential shear force that varies as sin(θ) or cos(θ) around the circumference is characteristic of this mode.

## A Practical Consideration

While an idealized bending load can be represented purely by the n=1 harmonic, a real-world load applied over a small area (like a bracket attached to a cylinder) will also excite higher-order harmonics (n=2,3,...).

So, for a complete analysis of a realistic load:

    You would use n=1 to capture the overall bending behavior of the structure.

    You might need to include higher harmonics to accurately model the local stresses and deformations right under the point of application.

And with increasing n the result will converge, right?

Yes, exactly. As you include more harmonics (increasing n), the solution will converge to the true 3D elasticity solution for the problem.

## The Principle of Convergence

The method is based on the Fourier series, which is a powerful mathematical tool capable of representing any reasonably well-behaved periodic function.

    The load applied to the structure is decomposed into a Fourier series. Adding more harmonics means you are creating a more accurate representation of the true load distribution.

    Since the structural response for each harmonic is solved correctly (within the 2D finite element approximation), a more accurate load model naturally leads to a more accurate final solution for displacements and stresses.

## Physical Interpretation and Practicality 🧑‍🔬

The convergence is typically quite fast due to the nature of the harmonics and Saint-Venant's principle:

    Low Harmonics (n=0,1): These capture the dominant, far-field behavior of the structure: uniform expansion/torsion (n=0) and overall bending (n=1).

    High Harmonics (n≥2): These represent more localized, rapidly varying deformation patterns (like ovalling, scalloping, etc.). The effects of these harmonics tend to decay quickly as you move away from the point of load application.

In practice, you only need to include enough harmonics to accurately model your load. For smooth loads like wind pressure, a few terms may be sufficient. For highly concentrated loads, more terms would be needed to capture the local stress concentration accurately.

Can you outline the numerical procedure to do a such an analysis?

Of course. Here is a step-by-step outline of the numerical procedure for this type of analysis.

## 1. Pre-processing

    Create 2D Mesh: First, create a standard 2D finite element mesh of the structure's cross-section in the r−z plane.

    Decompose the Load: Analyze your applied external load and decompose it into a Fourier series around the circumference (θ). This gives you the load amplitude functions (e.g., prn​(r,z)) for each required harmonic n.

    Compute Fundamental Matrices: For each element in the mesh, compute the three fundamental, harmonic-independent stiffness matrices: [K0​], [K1​], and [K2​]. This is done only once.

## 2. Analysis Loop 🔄

You then loop through each harmonic n that is significant for your decomposed load (e.g., n=0,1,2,...N).

For each harmonic n in the loop:

    Initialize Global Matrices: Create empty global matrices for the stiffness [Kn​] and force vector {Fn​}.

    Element Loop: For each element in the 2D mesh:

        Assemble Element Stiffness: Calculate the element stiffness matrix for the current harmonic using the pre-computed base matrices: [ke​]n​=[K0​]+n[K1​]+n2[K2​].

        Calculate Element Forces: Calculate the element's nodal force vector {Fn​}e​ by integrating the load amplitudes for harmonic n with the element's shape functions.

        Assemble into Global: Add the element matrices [ke​]n​ and {Fn​}e​ into the appropriate positions in the global matrices [Kn​] and {Fn​}.

    Apply Boundary Conditions: Modify the global system to account for any prescribed zero or non-zero displacements for the current harmonic n.

    Solve System: Solve the linear system of equations [Kn​]{un​}={Fn​} to find the vector of nodal displacement amplitudes {un​} for this harmonic.

    Store Results: Save the resulting displacement amplitudes {un​} and, if desired, calculate and save the stress amplitudes for this harmonic.

## 3. Post-processing

    Reconstruct Solution: After the analysis loop is complete, the final 3D displacement and stress fields are obtained by summing (superimposing) the results from each individual harmonic at any desired point (r,θ,z).

What are the K0, K1, K2 matrices?

The matrices [K0​], [K1​], and [K2​] are the three fundamental, harmonic-independent stiffness matrices for a single element. They are calculated once and then used to instantly generate the stiffness matrix for any harmonic n.

Their purpose is to separate the geometry-dependent parts of the stiffness calculation from the harmonic-dependent parts.

## The Stiffness Matrix Formula

The element stiffness matrix for any harmonic n, denoted [ke​]n​, is constructed using this simple quadratic formula:
[ke​]n​=[K0​]+n[K1​]+n2[K2​]

## Origin of Each Matrix

These matrices arise from expanding the integral for the element stiffness matrix after separating the strain-displacement matrix [Bn​] into its harmonic-independent part [BA​] and its linear-in-n part [BB​].

    [K₀]: The Base Stiffness Matrix
    [K0​]=∫V​[BA​]T[D][BA​]dV


    This matrix is derived from the parts of the strain calculation that do not have an explicit n coefficient. It is essentially the stiffness matrix you would use for a standard axisymmetric analysis (n=0).

    [K₁]: The Linear Coupling Matrix
    [K1​]=∫V​([BA​]T[D][BB​]+[BB​]T[D][BA​])dV


    This matrix represents the coupling between the base strain terms and the harmonic-dependent strain terms. It is the part of the stiffness that grows linearly with the harmonic number n.

    [K₂]: The Harmonic Stiffness Matrix
    [K2​]=∫V​[BB​]T[D][BB​]dV


    This matrix is derived purely from the parts of the strain calculation that are explicitly multiplied by n. It represents the stiffness that arises solely from the non-axisymmetric deformation modes and grows with the square of the harmonic number, n2.

Is there an N matrix? show me please this.

Yes, there is an [N] matrix. It's the standard matrix of shape functions used in the Finite Element Method.

Its purpose is to interpolate the displacement values from the nodes to any point within an element.

## The Shape Function Matrix [N]

The [N] matrix relates the continuous displacement field within an element, {u}, to the discrete vector of nodal displacements for that element, {ue​}.
$$\{u\} = [N] \{u_e\}$$In our semi-analytical method, this relationship applies to the **displacement amplitudes** for a specific harmonic $n$:$$\begin{Bmatrix} u_{rn}(r, z) \\ u_{\theta n}(r, z) \\ u_{zn}(r, z) \end{Bmatrix} = [N(r,z)] \begin{Bmatrix} u_{rn1} \\ u_{\theta n1} \\ u_{zn1} \\ \vdots \\ u_{rnm} \\ u_{\theta nm} \\ u_{znm} \end{Bmatrix}$$


Here, m is the number of nodes in the element (e.g., m=4 for a quadrilateral element).

The [N] matrix is constructed from the individual scalar shape functions Ni​(r,z), where i is the node number. It's arranged in a block-diagonal form. For an element with m nodes, it looks like this:
[N]=​N1​00​0N1​0​00N1​​⋯⋯⋯​Nm​00​0Nm​0​00Nm​​​


Each Ni​(r,z) is a standard 2D isoparametric shape function (e.g., bilinear for a 4-noded quad) that depends only on the local coordinates within the r−z plane.

How is B_A computed?

The matrix [BA​] is computed by applying a differential operator matrix, let's call it [LA​], to the shape function matrix [N].

This is the standard procedure for finding the strain-displacement matrix in any finite element analysis. The relationship is:
[BA​]=[LA​][N]

## The Differential Operator [LA​]

The [LA​] matrix contains the partial derivative operators that transform the displacement field into the strain field for the parts that are independent of the harmonic number n.

For the 3D axisymmetric case, the operator is a 6x3 matrix:
[LA​]=​∂r∂​r1​000∂z∂​​000∂r∂​−r1​∂z∂​0​00∂z∂​00∂r∂​​​

## How it Works

When you multiply [LA​] by the shape function matrix [N], you are essentially applying these derivatives to the shape functions. For a single node i, the resulting column in the [BA​] matrix looks like this:
​∂r∂Ni​​rNi​​∂z∂Ni​​∂r∂Ni​​−rNi​​∂z∂Ni​​∂z∂Ni​​+∂r∂Ni​​​​

Each row corresponds to a strain component:

    Row 1: Radial strain (ϵr​)

    Row 2: Hoop strain (ϵθ​)

    Row 3: Axial strain (ϵz​)

    Row 4: In-plane shear (γrθ​)

    Row 5: Transverse shear (γθz​)

    Row 6: Transverse shear (γzr​)

In short, [BA​] is simply the standard strain-displacement matrix you would compute for a regular 2D axisymmetric problem.

Sure? N is 3x3N, LA is 6x3 so the result should be 6x3N. BA should have 6x3 for each node.

You are absolutely correct. Thank you for the correction—my previous representation was an oversimplification. You are right about the dimensions.

The matrix [BA​] is indeed a 6 x (3 * m) matrix, where m is the number of nodes in the element. It's composed of m blocks, one for each node, with each block being a 6x3 matrix.

## The Correct Computation

Let's look at the computation for a single node i. The block [BAi​] is the result of multiplying the 6x3 operator [LA​] by the 3x3 shape function block for node i, [Ni​]:
[BAi​]=[LA​][Ni​]


Where:
[LA​]=​∂r∂​r1​000∂z∂​​000∂r∂​−r1​∂z∂​0​00∂z∂​00∂r∂​​​and[Ni​]=​Ni​00​0Ni​0​00Ni​​​


Performing this multiplication gives the correct 6x3 matrix block for node i:
[BAi​]=​∂r∂Ni​​rNi​​000∂z∂Ni​​​000∂r∂Ni​​−rNi​​∂z∂Ni​​0​00∂z∂Ni​​00∂r∂Ni​​​​

The full [BA​] matrix for the element is then formed by placing these blocks side-by-side:
[BA​]=[[BA1​]​[BA2​]​⋯​[BAm​]​]

So BA is largely similar to the B of the case n=0 but has additional terms b/c of the more complex strain situation

That's very close, but with one key distinction.

The matrix [BA​] is not just similar to the [B] matrix for the n=0 case; it is identical to it. It does not contain any additional terms.

The "additional terms" that arise from the more complex strain situation for n>0 are entirely captured in the other matrix, [BB​].

The whole point of the decomposition is to separate the problem cleanly:

    [BA​]: Contains the baseline, axisymmetric strain relationships.

    n[BB​]: Contains all the new, harmonic-dependent coupling terms.

So, the total strain-displacement matrix for any harmonic n is the sum of the simple axisymmetric part and the new harmonic-dependent part: [Bn​]=[BA​]+n[BB​].

But BA as shown is not correct for n=0. that only has 4 rows.

You are right again. This is an excellent point that highlights a subtle difference between how the n=0 case is often solved in practice versus how it's defined in this general framework. My apologies for the apparent contradiction.

Here is the clarification:

## Two Views of the Same Problem

    The Decoupled View (n=0 only): When you solve only the axisymmetric case, it's common and efficient to recognize that the problem splits into two completely independent parts:

        An in-plane problem (displacements ur​,uz​) with 4 strain components. The [B] matrix for this problem has 4 rows.

        A torsion problem (displacement uθ​) with 2 strain components.
        This is what I showed you initially and is why you are correct to say it has 4 rows.

    The General View (for n>0): For any harmonic n>0, all three displacement components (ur​,uθ​,uz​) are coupled, and all 6 strain components can be non-zero. Therefore, the strain-displacement matrix [Bn​] must have 6 rows.

## The Reconciliation

To create a consistent framework where [Bn​]=[BA​]+n[BB​], the baseline matrix [BA​] must also have 6 rows to match the dimensions of [Bn​].

The 6-row [BA​] matrix I showed you is the one that considers all 3 displacement directions simultaneously. If you use this specific [BA​] matrix to compute the stiffness matrix for the n=0 case, you will find that the resulting stiffness matrix is block-diagonal. One block will be the stiffness matrix for the 4-row in-plane problem, and the other block will be for the torsion problem.

So, while you can use a 4-row matrix for the isolated plane-strain/stress problem at n=0, the general theory uses the 6-row version of [BA​] so that it serves as a consistent baseline for all harmonics.

Understood!

Great! Let me know what you'd like to explore next.

The other B matrix, with the parts dependent on n

You're asking about the [BB​] matrix. This matrix is computed in the same way as [BA​], but with a different differential operator, [LB​].

The relationship is:
[BB​]=[LB​][N]


The purpose of [BB​] is to capture all the strain terms that are linearly dependent on the harmonic number n.

## The Differential Operator [LB​]

The [LB​] operator contains the coefficients of the terms that are multiplied by n in the strain-displacement equations. It is a 6x3 matrix:
[LB​]=​000−r1​00​0r1​0000​0000−r1​0​​

## The Resulting [BB​] Matrix

When you multiply [LB​] by the shape function matrix [N], you get the [BB​] matrix. The block for a single node i, [BBi​], is a 6x3 matrix:
[BBi​]=[LB​][Ni​]=​000−rNi​​00​0rNi​​0000​0000−rNi​​0​​


Each row corresponds to the part of the strain that scales with n:

    Row 2 (ϵθ​): Captures the hoop strain generated by tangential motion.

    Row 4 (γrθ​): Captures the in-plane shear generated by radial motion.

    Row 5 (γθz​): Captures the transverse shear generated by axial motion.

This [BB​] matrix isolates the unique coupling effects that only appear in non-axisymmetric (n>0) analysis.

Earlier I asked you "Now, how does this change for the case with n>0?"

In that answer you did not include the torsion (wasn't asked). Can you expand that answer about the torsional part please? Like give me the (epsilon_torsion,n) please, with explanation.

Of course. Let's expand on the torsional/shear part of the strain vector for a general harmonic, n>0.

In the axisymmetric case (n=0), the torsional strains only depended on the tangential displacement uθ​. For any harmonic where n>0, this is no longer true. The radial and axial displacements now also generate shear strains due to the twisting nature of the deformation. This is a key difference.

## Torsional/Shear Strains for a General Harmonic (n>0)

Here are the two shear strain components that make up what you called the "torsional part" of the strain vector, ϵtorsion,n​, for a general harmonic n.

    In-Plane Shear (γrθ​):
    This component represents the shear distortion in the r−θ plane (the cross-sectional plane).
    γrθ​=(∂r∂uθn​​−ruθn​+nurn​​)sin(nθ)


    Explanation:

        The first part, (∂r∂uθn​​−ruθn​​), is the familiar term from the n=0 case, representing shear from pure torsion.

        The new term, −rnurn​​, is crucial. It shows that for n>0, the radial displacement (urn​) now creates in-plane shear. As the cross-section deforms radially in a wavy pattern, it forces the material to shear.

    Transverse Shear (γθz​):
    This component represents the shear distortion in the θ−z plane.
    γθz​=(∂z∂uθn​​−rnuzn​​)sin(nθ)


    Explanation:

        The term ∂z∂uθn​​ is again the familiar part from the pure torsion case at n=0.

        The new term, −rnuzn​​, shows that the axial displacement (uzn​) now creates transverse shear. As the structure bends, the axial fibers stretch and compress in a wavy cos(nθ) pattern. This differential axial movement between adjacent circumferential points induces a shearing action. This is the primary shear effect in beam bending.

In summary, for any harmonic n>0, the problem becomes fully coupled. Unlike the simple axisymmetric case, the radial and axial displacements now directly contribute to the shear strains, linking bending and twisting phenomena together.

Just checking. This differentiation operator is for which order of the strains please?


$$[L_A] = \begin{bmatrix} \frac{\partial}{\partial r} & 0 & 0 \\ \frac{1}{r} & 0 & 0 \\ 0 & 0 & \frac{\partial}{\partial z} \\ 0 & \frac{\partial}{\partial r} - \frac{1}{r} & 0 \\ 0 & \frac{\partial}{\partial z} & 0 \\ \frac{\partial}{\partial z} & 0 & \frac{\partial}{\partial r} \end{bmatrix}$$

That operator corresponds to the following standard strain order:

    Radial Strain: ϵr​

    Hoop Strain: ϵθ​

    Axial Strain: ϵz​

    In-Plane Shear: γrθ​

    Transverse Shear: γθz​

    Transverse Shear: γzr​

Also in all this the order of the coordinates was r, theta, z right?

Yes, that's correct.

Throughout our discussion, we've consistently used the standard cylindrical coordinate system where the order is radius (r), angle (θ), and axis (z). All the vectors and operators have followed this convention.

Makes sense, this is a general cylindrical coordinate system.

Exactly. It's the standard convention used for these types of problems.

What would you like to cover next?

OK, I have the BA, BB matrices.

I assume, the D matrix will have to be updated as well. I have it for n=0, without torsion. The new one will be 6x6 with 5,5 and 6,6 being the same as 4,4

You're on the right track, and your assumption is correct for a standard isotropic material (like steel or aluminum), which is the most common case.

For the general analysis involving all 6 strain components, you need the full 6x6 constitutive matrix [D]. The key thing to remember is that for an isotropic material, this [D] matrix is constant and does not change with the harmonic number n. The complexity is all in the [B] matrix, not the [D] matrix.

## The 6x6 Constitutive Matrix [D]

The [D] matrix relates the stress vector to the strain vector: {σ}=[D]{ϵ}. For a linear, isotropic material, it is:
[D]=(1+ν)(1−2ν)E​​1−ννν000​ν1−νν000​νν1−ν000​00021−2ν​00​000021−2ν​0​0000021−2ν​​​


Here, E is Young's Modulus and ν is Poisson's ratio.

The lower-right 3x3 block contains the terms for the shear components. As you correctly deduced, for an isotropic material, these diagonal terms are all equal to the shear modulus, G:
D(4,4)=D(5,5)=D(6,6)=G=2(1+ν)E​


The term 21−2ν​ in the matrix is simply a result of factoring out the larger constant in front. Your intuition was spot on.

OK.

Now, computing the K0 matrix. Same as the n=0 case but B_A is used.

Yes, that's exactly right. The computation for [K0​] is identical to calculating the stiffness matrix for the standard axisymmetric (n=0) case, using the 6x6 formulation for the [BA​] and [D] matrices.

## Computing [K0​]

The formula for the [K0​] matrix is:
[K0​]=∫V​[BA​]T[D][BA​]dV


This volume integral is evaluated numerically using Gaussian quadrature. The process involves a change of variables from the global coordinates (r,z) to the element's local coordinates (ξ,η).

The differential volume element becomes:
dV=rdrdθdz=r(ξ,η)⋅∣J∣⋅dξdηdθ


where ∣J∣ is the determinant of the Jacobian matrix for the coordinate transformation.

The integration with respect to θ from 0 to 2π is done analytically and simply results in a factor of 2π. The final formula for numerical integration is:
[K0​]=2π∫−11​∫−11​[BA​]T(ξ,η)[D][BA​](ξ,η)r(ξ,η)∣J∣dξdη


This integral is then solved by evaluating the integrand at specific Gauss points within the element and summing the results with appropriate weights.

OK, going over to the K1 matrix.

The computation for the [K1​] matrix leads to a simple and elegant result: for an isotropic material, the [K1​] matrix is always a zero matrix.

## The Role of Orthogonality

The formula for [K1​] contains the cross-product terms between the harmonic-independent and harmonic-dependent parts of the strain:
[K1​]=∫V​([BA​]T[D][BB​]+[BB​]T[D][BA​])dV


The key here is the integration around the circumference (θ).

The strain components that make up [BA​] vary with cos(nθ), while the strain components that make up [BB​] vary with sin(nθ). Therefore, the integrand for [K1​] will contain products of these two functions: cos(nθ)sin(nθ).

Due to the orthogonality of trigonometric functions, the integral of this product over the full circumference is always zero:
∫02π​cos(nθ)sin(nθ)dθ=0


Because this integral is zero, the entire volume integral for [K1​] evaluates to zero.

This simplifies the final stiffness matrix formula significantly, leaving:
[ke​]n​=[K0​]+n2[K2​]

OK, how do I perform the integral?

I have this in my code:


K_contribution = 2 * sp.pi * (BA.T * D * BB + BB.T * D * BA) * r_physical_at_gp * det_J * w

You don't need to perform that integral because its result is analytically zero.

## The Source of the Zero

The calculation in your code, (BA.T * D * BB + BB.T * D * BA), represents the part of the integrand that depends on the 2D coordinates (r,z). However, you've missed the crucial trigonometric part that depends on θ.

The full integrand for the [K1​] matrix contains products of terms that vary as cos(nθ) (from [BA​]) and terms that vary as sin(nθ) (from [BB​]). So, before integrating over the 2D area, you must first integrate with respect to θ.

This leads to an integral of the form:
∫02π​cos(nθ)sin(nθ)dθ


This integral is identically zero for any integer n.

Because the integration with respect to θ yields zero, the entire volume integral for [K1​] becomes zero, regardless of the values of [BA​], [BB​], or [D].

In your code, you should not be multiplying by 2 * sp.pi. That factor comes from integrating cos2 or sin2, which only happens for the [K0​] and [K2​] matrices. For [K1​], the result of the theta integration is simply 0.

Therefore, you don't need a numerical loop for [K1​]; you can set it directly to a zero matrix.

How would I perform the integral? I understand the integral for K0 but not for K1. I'd like to see my code yielding that zero matrix.

Of course. Let's walk through how the integral for [K_1] results in a zero matrix from a computational perspective.

The reason you can't use the same integration approach as for [K_0] is that the result of the integration around the circumference (the theta direction) is not a constant like 2pi.

## The Full Integral

To see the result numerically, you have to consider the full integrand before integrating with respect to theta. The integrand for the [K_1] matrix involves the product of terms that vary with cos(ntheta) and terms that vary with sin(ntheta).

The integral for the contribution to [K_1] at a single Gauss point in your 2D mesh is conceptually:

K1_contribution = [ integral from 0 to 2*pi of (BA^T*D*BB + BB^T*D*BA) * cos(n*theta)*sin(n*theta) d(theta) ] * r * |J| * w

The matrix part, (BA^T*D*BB + BB^T*D*BA), is constant with respect to theta, so it can be pulled out of the theta integral:

K1_contribution = (BA^T*D*BB + BB^T*D*BA) * [ integral from 0 to 2*pi of cos(n*theta)*sin(n*theta) d(theta) ] * r * |J| * w

As we've discussed, that integral integral(cos*sin) is analytically zero.

## How to See This in Your Code

To have your code yield a zero matrix, you would need to perform the theta integration numerically inside your main loop. Here is what the logic would look like at a single Gauss point:
Python

# --- At a single Gauss Point in your existing loop ---
# You already have BA, BB, D, r_physical_at_gp, det_J, w

# 1. Calculate the matrix part of the integrand
K1_matrix_part = BA.T * D * BB + BB.T * D * BA

# 2. Numerically integrate the trigonometric part over theta
theta_integral = 0
num_theta_points = 100  # Number of steps for numerical integration
d_theta = 2 * sp.pi / num_theta_points
n = 1 # The harmonic number you are analyzing

for i in range(num_theta_points):
    theta = i * d_theta
    trig_term = sp.cos(n * theta) * sp.sin(n * theta)
    theta_integral += trig_term * d_theta

# 3. Check the result
# Because of numerical cancellation, theta_integral will be a very small number, like 1e-15, which is effectively zero.
# print(f"Numerical integral of cos*sin: {theta_integral}") 

# 4. Calculate the final contribution
K_contribution = K1_matrix_part * theta_integral * r_physical_at_gp * det_J * w

# Since theta_integral is zero, the entire K_contribution is a zero matrix.

Because the contribution at every single Gauss point is zero, the final assembled [K_1] matrix will be a zero matrix. This is why in practice, this loop is never written, and [K_1] is just set to zero directly.

Could you repeat this answer, using the more robust latex engine?

Of course. Here is that explanation again with the mathematical notations properly formatted.

You don't need to perform that integral because its result is analytically zero.

## The Source of the Zero

The calculation in your code, (BA.T * D * BB + BB.T * D * BA), represents the part of the integrand that depends on the 2D coordinates (r,z). However, this misses the crucial trigonometric part that depends on theta.

The full integrand for the [K_1] matrix contains products of terms that vary with cos(ntheta) (from [B_A]) and terms that vary with sin(ntheta) (from [B_B]). So, before integrating over the 2D area, you must first integrate with respect to theta.

The integral for the contribution to [K_1] at a single Gauss point in your 2D mesh is conceptually:

K1_contribution = [ int_02pi([B_A]T[D][B_B]+[B_B]T[D][B_A])cos(ntheta)sin(ntheta)dtheta ] * r|J|w

The matrix part is constant with respect to theta, so it can be pulled out of the theta integral:

K1_contribution = ([B_A]T[D][B_B]+[B_B]T[D][B_A]) * [ int_02picos(ntheta)sin(ntheta)dtheta ] * r|J|w

The integral intcos(ntheta)sin(ntheta)dtheta is analytically zero.

## How to See This in Your Code

To have your code yield a zero matrix, you would need to perform the theta integration numerically inside your main loop. Here is what the logic would look like at a single Gauss point:
Python

# --- At a single Gauss Point in your existing loop ---
# You already have BA, BB, D, r_physical_at_gp, det_J, w

# 1. Calculate the matrix part of the integrand
K1_matrix_part = BA.T * D * BB + BB.T * D * BA

# 2. Numerically integrate the trigonometric part over theta
theta_integral = 0
num_theta_points = 100  # Number of steps for numerical integration
d_theta = 2 * sp.pi / num_theta_points
n = 1 # The harmonic number you are analyzing

for i in range(num_theta_points):
    theta = i * d_theta
    # This is the cos(n*theta) * sin(n*theta) term
    trig_term = sp.cos(n * theta) * sp.sin(n * theta)
    theta_integral += trig_term * d_theta

# 3. Check the result
# Because of numerical cancellation, theta_integral will be a very 
# small number, like 1e-15, which is effectively zero.
# print(f"Numerical integral of cos*sin: {theta_integral}") 

# 4. Calculate the final contribution
K_contribution = K1_matrix_part * theta_integral * r_physical_at_gp * det_J * w

# Since theta_integral is zero, the entire K_contribution is a zero matrix.

Because the contribution at every single Gauss point is zero, the final assembled [K_1] matrix will be a zero matrix. This is why in practice, this loop is never written, and [K_1] is just set directly to zero.

Still not good, maye even worse!

I sincerely apologize. It's clear my explanations have been confusing and unhelpful. Let me try a much more direct approach.

The entire problem comes down to one number in your line of code: the 2 * sp.pi.

That number is the result of an integral around the circumference, and it's different for each K matrix.

    For [K₀]: The integral involves terms like 1×1. The result is 2π. Your factor is correct.

    For [K₂]: The integral involves terms like cos2(nθ). The result is π.

    For [K₁]: The integral involves terms like cos(nθ)×sin(nθ). The result is 0.

Therefore, the factor you should be multiplying by for the K₁ matrix is zero.

Your line of code for the K₁ contribution should be:
K_contribution = (BA.T * D * BB + BB.T * D * BA) * 0 * r_physical_at_gp * det_J * w

Which means the contribution is always zero. You don't need to compute the matrices at all; the result for [K1​] is simply a matrix full of zeros.

OK, I'll get back to this.

so for K2 I have this: K_contribution = sp.pi * BB.T * D * BB * r_physical_at_gp * det_J * w

Yes, that's exactly right.

Your formula for the [K2​] contribution is correct.

The sp.pi factor is correct because it's the result of integrating terms like cos2(nθ) or sin2(nθ) around the circumference for any harmonic n≥1. The rest of the expression correctly represents the matrix integrand for [K2​] evaluated at a Gauss point.

OK. Show me please in detail the K2 integral. I'd like to understand this thing with the triginometric terms.

Sure, here is a detailed breakdown of the integral for the [K2​] matrix, focusing on the trigonometric terms.

## The Integral Formula

The starting point is the definition of the [K2​] matrix:
[K2​]=∫V​[BB​]T[D][BB​]dV


The key is to remember what the matrices inside this integral represent. The matrix [BB​] gives the amplitudes of the strains that are linear in n. The full strains are these amplitudes multiplied by their corresponding trigonometric function, either cos(nθ) or sin(nθ).

## The Trigonometric Products

When we form the matrix product [BB​]T[D][BB​], we are effectively creating a sum of terms where each term is a product of two strain amplitudes multiplied by a material property from [D]. The full expression, before integrating over θ, will also contain the product of the corresponding trigonometric functions.

For an isotropic material, the [D] matrix is structured such that it does not couple normal strains (like ϵθ​) with shear strains (like γrθ​).

    The strain amplitude related to ϵθ​ in [BB​] is associated with cos(nθ).

    The strain amplitudes related to γrθ​ and γθz​ in [BB​] are associated with sin(nθ).

Because they are not coupled by the [D] matrix, the integrand will only contain terms that look like:

    (stuff)×cos2(nθ)

    (other stuff)×sin2(nθ)

You will not have any cross-terms like cos(nθ)sin(nθ).

## Integration Over the Circumference

The next step is to integrate these trigonometric terms with respect to θ from 0 to 2π. For any harmonic n≥1, these integrals yield the same constant value:
∫02π​cos2(nθ)dθ=π
∫02π​sin2(nθ)dθ=π


Because every term in the integrand is multiplied by a trigonometric part that integrates to π, the entire integration over θ simplifies to a single constant factor of π.

## The Final Numerical Integral

This simplifies the volume integral down to a 2D integral over the element's area, which is then solved numerically:
[K2​]=π∫−11​∫−11​[BB​]T(ξ,η)[D][BB​](ξ,η)r(ξ,η)∣J∣dξdη


This is why your line of code K_contribution = sp.pi * BB.T * D * BB * ... is correct. The sp.pi factor is the result of analytically integrating the squared trigonometric terms around the circumference.

Stupid question coming. Where is theta and the sin / cos in the B matrices?

That's not a stupid question at all; it's a key concept of this semi-analytical method.

The theta, sin(n*theta), and cos(n*theta) terms are not inside the [B] matrices.

The entire method is built on separating the problem:

    The [B] matrices only handle the geometry in the 2D plane (r,z). They relate the displacement amplitudes to the strain amplitudes, which only depend on r and z.

    The trigonometric functions (sin and cos) describe how those amplitudes are distributed around the circumference (θ).

The two parts are kept separate until the final step of calculating the stiffness matrix, where the trigonometric functions are handled by the integral around the circumference, resulting in the constant factors like π or 0.

OK. Now, having the K0, K2 matrices, I see that the terms of the K2 are by orders of magnitude smaller, than those of K0. What does this mean physically?

That's an excellent observation with a direct physical meaning.

The [K₀] matrix represents the primary stiffness of the material from being stretched and sheared in its cross-section (the r−z plane). This is the dominant way a structure resists loads.

The [K₂] matrix, on the other hand, represents a secondary stiffness that arises purely from the curvature of the structure. It captures the complex coupling between displacement directions that only exists in non-axisymmetric deformation modes.

## [K₀]: The Primary Stiffness

This matrix contains terms related to derivatives like ∂r∂​ and ∂z∂​. Physically, this represents the significant energy stored when the material fibers are stretched or sheared. This is the fundamental material stiffness, analogous to the membrane and bending stiffness of a flat plate.

## [K₂]: The Curvature-Induced Stiffness

This matrix contains terms related only to r1​. It does not involve any direct derivatives of the shape functions. Physically, this represents the energy stored due to the geometric coupling of the displacement fields because the structure is circular. For example, it captures how radial motion creates shear in a non-axisymmetric mode. This is often a less dominant mechanism for storing energy, which is why the terms in [K2​] are generally smaller than those in [K0​].

## The Role of n2

While the entries of [K2​] may be small, its contribution to the total stiffness is scaled by n2:
[ke​]n​=[K0​]+n2[K2​]


This means for higher-order deformation modes (like ovalling at n=2 or lobing at n=3,4,...), the contribution from [K2​] becomes very significant. The structure becomes progressively stiffer as you try to deform it into more complex circumferential patterns.

Do I ever need to sum the B_A and B_B matrices?

No, not for calculating the stiffness matrix, but yes, for calculating the stresses.

## For the Stiffness Matrix

You never explicitly sum [BA​] and [BB​] to get the stiffness matrix. Instead, you use them separately to compute the fundamental matrices [K0​] and [K2​]. The final element stiffness matrix for any harmonic n is then assembled from those results:
[ke​]n​=[K0​]+n2[K2​]

## For Stress Calculation

After you've solved for the nodal displacement amplitudes {un​}, you need to calculate the strains to find the stresses. The strain amplitudes for a given harmonic are found using:
$$\{\epsilon_n\} = [B_n] \{u_n\}$$To get the $[B_n]$ matrix for the specific harmonic you're analyzing, you must compute the sum:$$[B_n] = [B_A] + n[B_B]$$


This is typically done at the element's Gauss points during post-processing.

OK, thank you. Today you really helped me a lot.

One more question: which book would be the best resource for this topic?

You're very welcome! I'm glad I could help.

For this specific topic, the classic and most authoritative resource is the book by Zienkiewicz.

## Primary Recommendation

Title: The Finite Element Method: Its Basis and Fundamentals
Authors: O.C. Zienkiewicz, R.L. Taylor, and J.Z. Zhu

Why it's the best: This book is often called the "bible" of the finite element method. It is incredibly comprehensive and provides a rigorous, detailed derivation of the semi-analytical method for axisymmetric problems. The chapter on the analysis of solids will contain the exact theory we've been discussing, including the decomposition of the stiffness matrix.

## Other Excellent Resources

If you want alternatives, these are also considered cornerstone texts in the field:

    Concepts and Applications of Finite Element Analysis by R.D. Cook et al.: Another classic textbook known for its clear explanations and practical focus. It presents the theory very well.

    Finite Element Procedures by K.J. Bathe: A very rigorous and mathematically precise text with a strong focus on the computational procedures and algorithms.

The Zienkiewicz book is the most direct and complete reference for this specific subject, but any of these three will be an excellent resource for a deeper understanding.

Happy reading! 📚

Can you check values numerically? Or do you have a benchmark problem for this?

I can't execute a numerical solver to check values myself, but I can provide a classic benchmark problem that is perfect for validating your code.

## Numerical Capabilities

As a language model, I don't have the ability to run external software like a finite element solver. My capabilities are limited to processing and generating text and code.

However, I can help you analyze your code, generate scripts, and check your mathematical formulations, as we have been doing.

## Classic Benchmark Problem: Cylinder in Bending 🎯

A well-established benchmark for this semi-analytical method is a simply supported or cantilevered cylinder subjected to a non-axisymmetric load. This problem allows you to check your implementation against known analytical solutions.

Problem Setup

    Geometry: A cylinder or pipe with a defined length (L), radius (R), and wall thickness (t).

    Material: A standard isotropic material with Young's Modulus (E) and Poisson's ratio (ν).

    Boundary Conditions:

        Cantilevered: Fixed at one end (z=0), free at the other (z=L).

        Simply Supported: Pinned at both ends.

    Load Case: The key is to use a load that has a simple Fourier series representation. The best example is a sinusoidal pressure distribution that mimics wind load:
    pr​(θ)=−p0​cos(θ)


    This pressure is applied along the length of the cylinder.

Why It's a Good Benchmark

    Pure Harmonic: This load is represented perfectly by a single harmonic, n=1. You don't need to sum multiple harmonics, making it ideal for verifying that your K₀, K₂, and load vector for n=1 are implemented correctly.

    Analytical Solution: For a thin-walled cylinder that behaves like a beam, you can compare the results (like the deflection at the free end of a cantilever) to the solution from classical beam theory. The total force on the cylinder from this pressure distribution can be calculated, and the deflection can be found using formulas like PL3/(3EI).

    Stress Verification: You can also compare the maximum axial stress (σz​) at the fixed end with the bending stress from beam theory, σ=My/I.

By running this simple n=1 problem, you can gain a high degree of confidence that your implementation of the core matrices and solution procedure is correct.

Good idea. But for that I need the loads implemented, too. Let's do that tomorrow.

Sounds good. I'll be ready when you are. Have a good night!

Can I export this whole conversation?

Yes, you have a couple of options to save or export our conversation.

## Option 1: Share a Public Link

This is the quickest way to save a snapshot of the conversation that you can bookmark or share with others.

    At the top of the chat, find the Share & export option (it might be under the ⋮ menu).

    Click Share.

    A public link will be created. Anyone with this link can view the conversation, but it won't be linked to your Google Account.

## Option 2: Google Takeout

If you want a complete archive of all your Gemini activity for your own records, you can use Google Takeout.

This service allows you to download your data from all Google products, including your entire Gemini chat history. The data is typically exported in formats like JSON and HTML.

You can access it here: takeout.google.com
Google Privacy Policy Opens in a new window
Google Terms of Service Opens in a new window
Your privacy & Gemini Apps Opens in a new window

Gemini may display inaccurate info, including about people, so double-check its responses.
