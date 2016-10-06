require 'spec_helper'

describe package('python3') do
  it { should be_installed }
end

describe package('python3-pip') do
  it { should be_installed }
end

describe package('python3-dev') do
  it { should be_installed }
end

describe package('libpq-dev') do
  it { should be_installed }
end
