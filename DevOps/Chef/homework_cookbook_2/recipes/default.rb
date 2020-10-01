
package 'Install Apache' do
  package_name 'httpd'
end

template '/var/www/html/index.html' do
  source 'index.html.erb'
  owner 'apache'
  group 'apache'
  mode '0755'
  variables(ip_address: node['ipaddress'],
            host_name: node['hostname'])
  notifies :restart, 'service[httpd]', :immediately
end

service 'httpd' do
  action :nothing
end