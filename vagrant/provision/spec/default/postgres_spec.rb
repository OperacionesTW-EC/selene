require 'spec_helper'

describe package('postgresql') do
  it { should be_installed }
end

describe package('python-psycopg2') do
  it { should be_installed }
end

describe package('acl') do
  it { should be_installed }
end

describe port(5432) do
  it { should be_listening }
end

describe file('/etc/postgresql/9.1/main/pg_hba.conf') do
  it 'should disable peer connection for postgres user' do
    should_not contain 'local   all             postgres                                peer'
  end

  it 'should enable md5 connection for postgres user' do
    should contain 'local   all             postgres                                md5'
  end
end

describe command('PGPASSWORD=postgres psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname=\'selene\'"') do
  its (:stdout) { should match /1/ }
end
