
interfaces = ""
node["network"]["interfaces"].keys.each do |interface|
  interfaces = interfaces + interface + "\n"
end
file "/tmp/interfaces.txt" do 
  content interfaces
end
