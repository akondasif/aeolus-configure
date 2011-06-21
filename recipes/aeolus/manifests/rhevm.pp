class aeolus::rhevm inherits aeolus  {
  file {"/etc/rhevm.json":
    content => template("aeolus/rhevm.json"),
    mode => 755,
    require => Package['aeolus-conductor-daemons'] }

  file {"/etc/iwhd/conf.js":
    content => template("aeolus/iwhd-conf.js"),
    mode => 755,
    require => Package['aeolus-conductor-daemons'] }

  file {"$rhevm_nfs_mount_point":
    ensure => 'directory'}

  mount {"$rhevm_nfs_mount_point":
    ensure => mounted,
    device => "$rhevm_nfs_server:$rhevm_nfs_export",
    fstype => "nfs",
    options => "rw",
    require => File["$rhevm_nfs_mount_point"]}

  # give iwhd a restart to pick up new configuration files
  # in the event iwhd had already initialized at /var/lib/iwhd
  exec { "/sbin/service iwhd restart":
    require => [Service['iwhd'],
                Mount["$rhevm_nfs_mount_point"],
                File["/etc/rhevm.json"],
                File["/etc/iwhd/conf.js"]]}

  aeolus::deltacloud{"rhevm":
    provider_type => 'rhevm',
    endpoint => "$rhevm_deltacloud_powershell_url",
    port => $rhevm_deltacloud_port}

  aeolus::conductor::provider{"rhevm":
    type           => "rhevm",
    url            => "http://localhost:${rhevm_deltacloud_port}/api",
    require        => Aeolus::Deltacloud["rhevm"]}

  # TODO:
  # 1. since we have credentials, create provider account
  # 2. create a realm and mappings
}

class aeolus::rhevm::disabled {
  aeolus::deltacloud::disabled{"rhevm": }

  mount {"$rhevm_nfs_mount_point":
    ensure => unmounted,
    device => "$rhevm_nfs_server:$rhevm_nfs_export"}
}