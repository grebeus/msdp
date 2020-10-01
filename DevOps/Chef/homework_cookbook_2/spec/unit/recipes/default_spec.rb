
require 'spec_helper'

describe 'homework_cookbook_2::default' do
    let(:chef_run) {
      ChefSpec::SoloRunner.new(platform: 'centos', version: '7').converge(described_recipe)
    }

    it 'Installs Apache' do
      expect(chef_run).to install_package('httpd')
    end

    it 'Creates template' do
      expect(chef_run).to create_template('/var/www/html/index.html').with(
        owner: 'apache',
        group: 'apache',
        mode: '0755'
      )
      expect(chef_run).to render_file('/var/www/html/index.html').with_content('Host Details')
    end

    let(:template) { chef_run.template('/var/www/html/index.html') }

    it 'Sends notification immediately' do
      expect(template).to notify('service[httpd]').immediately
      expect(template).to_not notify('service[not_httpd]').immediately
    end

    it 'Sends notification immediately' do
      expect(template).to notify('service[httpd]').to(:restart).immediately
      expect(template).to_not notify('service[httpd]').to(:restart).delayed
    end

    it 'Executes nothing' do
      service = chef_run.service('httpd')
      expect(service).to do_nothing
    end
end
