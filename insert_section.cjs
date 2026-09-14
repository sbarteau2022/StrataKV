const fs = require('fs');
const content = fs.readFileSync('src/components/MarketingDeck.tsx', 'utf-8');

const newSection = `
      {/* SLIDE 1.5: THE PLAIN LANGUAGE BREAKDOWN */}
      <section className="max-w-6xl mx-auto px-6 py-12 lg:py-24">
        <div className="text-center space-y-4 mb-16">
          <h2 className="font-serif text-3xl md:text-5xl text-[var(--color-ivory)]">The Big Picture</h2>
          <p className="text-[var(--color-muted)] text-lg max-w-2xl mx-auto">
            Breaking down the StrataKV breakthrough in plain English.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="glass-card p-8 rounded-2xl space-y-4 border-t-2 border-t-[var(--color-gold)]">
            <div className="w-12 h-12 rounded-full bg-[rgba(221,194,140,0.1)] flex items-center justify-center text-[var(--color-gold)] font-bold text-xl mb-6">1</div>
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">What We Did</h3>
            <p className="text-[var(--color-muted)] leading-relaxed">
              We completely redesigned how AI agents remember things. Standard AI models blindly memorize everything until they run out of memory and crash. We built StrataKV—a "breathing" memory engine that permanently pins core instructions while actively exhaling useless noise (like old tool logs).
            </p>
          </div>

          <div className="glass-card p-8 rounded-2xl space-y-4 border-t-2 border-t-[var(--color-success)]">
            <div className="w-12 h-12 rounded-full bg-[rgba(184,205,177,0.1)] flex items-center justify-center text-[var(--color-success)] font-bold text-xl mb-6">2</div>
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">Why It Matters</h3>
            <p className="text-[var(--color-muted)] leading-relaxed">
              Until now, running autonomous AI agents meant paying massive cloud bills or watching your local computer crash from "Out of Memory" errors. Our breakthrough allows highly complex AI swarms to run forever on consumer hardware securely, privately, and for zero recurring cost.
            </p>
          </div>

          <div className="glass-card p-8 rounded-2xl space-y-4 border-t-2 border-t-[var(--color-silver)]">
            <div className="w-12 h-12 rounded-full bg-[rgba(216,223,225,0.1)] flex items-center justify-center text-[var(--color-silver)] font-bold text-xl mb-6">3</div>
            <h3 className="font-serif text-2xl text-[var(--color-ivory)]">What Comes Next</h3>
            <p className="text-[var(--color-muted)] leading-relaxed">
              We are scaling the system to support entire swarms of collaborative agents orchestrated by the Elle Conductor. Soon, developers will be able to deploy sovereign, uncensorable AI systems that can independently manage codebases, servers, and operations indefinitely.
            </p>
          </div>
        </div>
      </section>
`;

const updatedContent = content.replace('{/* SLIDE 2: PRINCIPLED INTELLIGENCE */}', newSection + '\n      {/* SLIDE 2: PRINCIPLED INTELLIGENCE */}');

fs.writeFileSync('src/components/MarketingDeck.tsx', updatedContent);
console.log('Successfully injected the plain language section');
