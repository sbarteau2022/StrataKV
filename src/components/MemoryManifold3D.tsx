import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export const MemoryManifold3D: React.FC = () => {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const currentMount = mountRef.current;
    if (!currentMount) return;

    const width = currentMount.clientWidth || 480;
    const height = 340;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 0, 21);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    currentMount.appendChild(renderer.domElement);

    // 2. Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xDDC28C, 2.5, 50);
    pointLight.position.set(5, 10, 10);
    scene.add(pointLight);

    const cyanLight = new THREE.PointLight(0xB8CDB1, 2, 50);
    cyanLight.position.set(-5, -5, 5);
    scene.add(cyanLight);

    // 3. Tier 1: Pinned Invariant Core (Golden Torus + Sphere)
    const tier1Group = new THREE.Group();

    const coreGeo = new THREE.SphereGeometry(1.8, 32, 32);
    const coreMat = new THREE.MeshStandardMaterial({
      color: 0xDDC28C,
      emissive: 0x715534,
      roughness: 0.2,
      metalness: 0.85,
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    tier1Group.add(coreMesh);

    const ringGeo = new THREE.TorusGeometry(3.6, 0.12, 16, 100);
    const ringMat = new THREE.MeshStandardMaterial({
      color: 0xDDC28C,
      roughness: 0.3,
      metalness: 0.9,
    });
    const ringMesh1 = new THREE.Mesh(ringGeo, ringMat);
    ringMesh1.rotation.x = Math.PI / 2;
    tier1Group.add(ringMesh1);

    const ringMesh2 = new THREE.Mesh(ringGeo, ringMat);
    ringMesh2.rotation.x = Math.PI / 3;
    ringMesh2.rotation.y = Math.PI / 6;
    tier1Group.add(ringMesh2);

    scene.add(tier1Group);

    // 4. Tier 2: Harmonic Superposition Basin (Torus with 12 spheres)
    const tier2Group = new THREE.Group();
    
    // The main Torus for Tier 2
    const tier2TorusGeo = new THREE.TorusGeometry(6.2, 0.08, 16, 100);
    const tier2TorusMat = new THREE.MeshBasicMaterial({
      color: 0xB8CDB1,
      transparent: true,
      opacity: 0.45,
    });
    const tier2TorusMesh = new THREE.Mesh(tier2TorusGeo, tier2TorusMat);
    tier2TorusMesh.rotation.x = Math.PI / 2; // Lay flat
    tier2Group.add(tier2TorusMesh);

    // 12 Spheres snapped to the Torus
    const nodeGeo = new THREE.SphereGeometry(0.4, 16, 16);
    const nodeMat = new THREE.MeshStandardMaterial({ 
      color: 0xF0EADD, 
      emissive: 0xDDC28C, 
      emissiveIntensity: 0.5,
      roughness: 0.1 
    });
    
    for (let i = 0; i < 12; i++) {
      const angle = (i / 12) * Math.PI * 2;
      const radius = 6.2;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      
      const node = new THREE.Mesh(nodeGeo, nodeMat);
      node.position.set(x, 0, z); // Snapped onto the flat Torus
      tier2Group.add(node);
    }

    scene.add(tier2Group);

    // 5. Tier 3: Dissipative Exhalation Cloud (Golden Ratio Spiral Particles)
    const particleCount = 280;
    const particleGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const phi = 1.61803398875;

    for (let i = 0; i < particleCount; i++) {
      const theta = i * 0.18;
      const r = 4.5 + Math.pow(i / particleCount, 0.8) * 7.5;
      const x = r * Math.cos(theta * phi);
      const z = r * Math.sin(theta * phi);
      const y = (Math.random() - 0.5) * 4.0;

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0xD8DFE1,
      size: 0.22,
      transparent: true,
      opacity: 0.65,
    });
    const particleSystem = new THREE.Points(particleGeo, particleMat);
    scene.add(particleSystem);

    // 6. Interactive Mouse Drag to Rotate
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;
    let targetRotationX = 0.05;
    let targetRotationY = 0;

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMouseX;
      const deltaY = e.clientY - prevMouseY;
      targetRotationY += deltaX * 0.008;
      targetRotationX += deltaY * 0.008;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseUp = () => { isDragging = false; };

    const domElement = renderer.domElement;
    domElement.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    // 7. Animation Loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      // Smooth rotation
      tier1Group.rotation.y += 0.012;
      tier1Group.rotation.x += 0.005;

      tier2Group.rotation.y -= 0.006;
      tier2Group.rotation.z += 0.003;

      particleSystem.rotation.y += 0.004;

      // Apply drag interaction with damping
      scene.rotation.y += (targetRotationY - scene.rotation.y) * 0.08;
      scene.rotation.x += (targetRotationX - scene.rotation.x) * 0.08;

      renderer.render(scene, camera);
    };
    animate();

    // 8. Handle Resize
    const handleResize = () => {
      if (!currentMount) return;
      const newWidth = currentMount.clientWidth;
      camera.aspect = newWidth / height;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, height);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      cancelAnimationFrame(animationFrameId);
      domElement.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      window.removeEventListener('resize', handleResize);
      if (currentMount && renderer.domElement) {
        currentMount.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  return (
    <div className="relative w-full overflow-hidden rounded-2xl border border-[rgba(121,121,107,0.35)] bg-[rgba(16,18,15,0.7)] backdrop-blur-md p-4">
      <div className="flex justify-between items-center mb-2 px-2">
        <div>
          <span className="text-xs uppercase tracking-widest text-[var(--color-gold)] font-mono font-semibold">WebGL 3D Memory Manifold</span>
          <div className="text-xs text-[var(--color-muted)]">Interactive 3-Tier KV Superposition • Drag to Orbit</div>
        </div>
        <div className="flex items-center gap-3 text-[11px] font-mono text-[var(--color-muted)]">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-[var(--color-gold)]"></span> Tier 1 Core</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-[var(--color-success)]"></span> Tier 2 Superposition</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-[var(--color-silver)]"></span> Tier 3 Exhale</span>
        </div>
      </div>
      <div ref={mountRef} className="w-full h-[340px] cursor-grab active:cursor-grabbing flex items-center justify-center" />
    </div>
  );
};
