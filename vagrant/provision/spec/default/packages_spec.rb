require 'spec_helper'

describe package('python3') do
  it { should be_installed }
end
