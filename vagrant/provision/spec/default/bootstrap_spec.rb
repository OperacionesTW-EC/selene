require 'spec_helper'

describe file('/etc/environment') do
  it { should contain 'DB_1_ENV_POSTGRES_DB=selene'}
  it { should contain 'DB_1_ENV_POSTGRES_USER=postgres'}
  it { should contain 'DB_1_ENV_POSTGRES_PASSWORD=postgres'}
  it { should contain 'DB_PORT_5432_TCP_ADDR=127.0.0.1'}
  it { should contain 'DB_PORT_5432_TCP_PORT=5432'}
end
