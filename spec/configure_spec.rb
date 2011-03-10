require 'spec_helper'

require 'nokogiri'
require 'open-uri'
require 'postgres'

ENV['RAILS_ENV'] = 'production'
$: << "#{CONDUCTOR_PATH}/dutils"
require "dutils"

describe "aeolus-configure" do
  before(:all) do
    # !!! need to comment out "#Defaults    requiretty" via visudo for this to work remotely
    `sudo /usr/sbin/aeolus-configure`
    $?.exitstatus.should == 0
  end

  it "should install all aeolus packages" do
    (AEOLUS_PACKAGES + AEOLUS_DEPENDENCY_PACKAGES).each { |pkg|
      `/bin/rpm -q #{pkg}`
      $?.exitstatus.should be(0), "package '#{pkg}' should be installed but it is not"
    }
  end

  it "should start all aeolus services" do
   (AEOLUS_SERVICES + AEOLUS_DEPENDENCY_SERVICES).each { |srv|
     `/sbin/service #{srv} status`
      $?.exitstatus.should be(0), "service '#{srv}' should be running but it is not"
   }
  end

  it "should correctly create an aeolus templates bucket" do
    doc = Nokogiri::HTML(open(IWHD_URI))
    doc.xpath("//html/body/api/link[@rel='bucket' and @href='#{IWHD_URI}templates']").size.should == 1
  end

  it "should properly setup the postgres db and user" do
    PGconn.open('user=aeolus dbname=conductor').should_not raise_error(PGError)
  end

  it "should create a site admin for aeolus conductor" do
    User.find(:first, :conditions => ["login = 'admin' AND " +
                                      "email = 'dcuser@aeolusproject.org' AND " +
                                      "first_name = 'aeolus' AND " +
                                      "last_name = 'user'"]).should_not be_nil
  end

  it "should open the necessary firewall ports" do
    FIREWALL_OPEN_PORTS.each { |port|
      output = `sudo iptables -nvL | grep "tcp dpt:#{port}"`
      output.should_not eql(""), "port '#{port}' should be open but it is not"
    }
  end

  it "should properly setup apache httpd" do
    # TODO when we re-enable security, test https here
    doc = Nokogiri::HTML(open(CONDUCTOR_URI + "/login"))
    node = doc.xpath("//html/head/title").first
    node.content.should =~ /.*Red Hat Cloud Engine.*/
  end

end