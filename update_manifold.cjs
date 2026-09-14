const fs = require('fs');

let content = fs.readFileSync('src/components/MemoryManifold3D.tsx', 'utf-8');

// Replace the Tier 2 section completely
const tier2Regex = /\/\/ 4\. Tier 2: Harmonic Superposition Basin[\s\S]*?\/\/ 5\. Tier 3: Dissipative Exhalation/m;

const newTier2 = `// 4. Tier 2: Harmonic Superposition Basin (Torus with 12 spheres)
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

    // 5. Tier 3: Dissipative Exhalation`;

content = content.replace(tier2Regex, newTier2);

fs.writeFileSync('src/components/MemoryManifold3D.tsx', content);
console.log('Manifold updated');
