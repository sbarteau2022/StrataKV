with open('/Users/stewartbarteau/Desktop/stratakv/benchmarks/generate_multitier_suite.py', 'r') as f:
    content = f.read()

# Replace html += """    </div> with html += f"""    </div>
content = content.replace('html += """    </div>\n\n  </section>\n\n  <!-- ===', 'html += f"""    </div>\n\n  </section>\n\n  <!-- ===')

with open('/Users/stewartbarteau/Desktop/stratakv/benchmarks/generate_multitier_suite.py', 'w') as f:
    f.write(content)

print("Updated generate_multitier_suite.py with f-string for tier3/4")
