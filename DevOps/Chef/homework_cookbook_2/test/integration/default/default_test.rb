
describe package('httpd') do
  it { should be_installed }
end

describe file('/var/www/html/index.html') do
  it { should exist }
  its ('content') { should match /Host Details/ }
  its ('content') { should match sys_info.ip_address }
  its ('content') { should match sys_info.short }
end

describe service('httpd') do
  it { should be_running }
end