%bcond check 1
%global debug_package %{nil}

Name:           goose
Version:        1.19.0
Release:        %autorelease
Summary:        an open source, extensible AI agent client
URL:            https://github.com/block/goose
Source:         %{url}/archive/v%{version}/goose-%{version}.tar.gz

# Patches to remove windows dependencies from the crates
Patch:          0001-Remove-windows-cfg-from-Cargo.toml.patch

License:  %{shrink:
    (Apache-2.0 OR MIT) AND BSD-3-Clause
    (MIT OR Apache-2.0) AND NCSA
    (MIT OR Apache-2.0) AND Unicode-3.0
    0BSD OR MIT OR Apache-2.0
    Apache-2.0
    Apache-2.0 OR BSL-1.0
    Apache-2.0 OR ISC OR MIT
    Apache-2.0 OR MIT
    Apache-2.0 WITH LLVM-exception
    Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
    BSD-2-Clause
    BSD-2-Clause OR Apache-2.0 OR MIT
    BSD-3-Clause
    BSD-3-Clause AND MIT
    BSD-3-Clause OR MIT
    BSL-1.0
    CC0-1.0
    CC0-1.0 OR Apache-2.0
    CC0-1.0 OR Apache-2.0 OR Apache-2.0 WITH LLVM-exception
    CC0-1.0 OR MIT-0 OR Apache-2.0
    ISC
    ISC AND (Apache-2.0 OR ISC)
    ISC AND (Apache-2.0 OR ISC) AND OpenSSL
    LGPL-3.0-or-later
    MIT
    MIT AND BSD-3-Clause
    MIT OR Apache-2.0
    MIT OR Apache-2.0 OR Zlib
    MIT OR Zlib OR Apache-2.0
    MIT-0
    MPL-2.0
    Unicode-3.0
    Unlicense OR MIT
    Zlib
    Zlib OR Apache-2.0 OR MIT
}

BuildRequires: cargo-rpm-macros >= 25
BuildRequires: systemd
BuildRequires: openssl-devel
BuildRequires: cmake
BuildRequires: clang-libs
BuildRequires: clang
BuildRequires: libxcb-devel
BuildRequires: tomcli

%global _description %{expand:
an open source, extensible AI agent that goes beyond code suggestions - install, execute, edit, and test with any LLM.}

%description %_description

%prep
%autosetup -n %{name}-%{version} -p1

# Relax dependency for which
# TODO(r0x0d): This can probably be updated in upstream
tomcli set crates/goose/Cargo.toml str dependencies.which ">=7.0.0,<=8.0.0"

# Relax dependency for webbrowser
# TODO(r0x0d): This can be updated in upstream to use 1.0.0.
tomcli set crates/goose/Cargo.toml str dependencies.webbrowser ">=0.8.0,<=1.0.6"
tomcli set crates/goose-mcp/Cargo.toml str dependencies.webbrowser ">=0.8.0,<=1.0.6"

# Relax treesitter dependencies
tomcli set crates/goose-mcp/Cargo.toml str dependencies.tree-sitter ">=0.21,<=0.25"
tomcli set crates/goose-mcp/Cargo.toml str dependencies.tree-sitter-go ">=0.21,<=0.25"
tomcli set crates/goose-mcp/Cargo.toml str dependencies.tree-sitter-java ">=0.21,<=0.25"
tomcli set crates/goose-mcp/Cargo.toml str dependencies.tree-sitter-javascript ">=0.21,<=0.25"
tomcli set crates/goose-mcp/Cargo.toml str dependencies.tree-sitter-python ">=0.21,<=0.25"
tomcli set crates/goose-mcp/Cargo.toml str dependencies.tree-sitter-ruby ">=0.21,<=0.25"
tomcli set crates/goose-mcp/Cargo.toml str dependencies.tree-sitter-rust ">=0.21,<=0.25"

# Relax dependency for sysinfo
tomcli set crates/goose-mcp/Cargo.toml str dependencies.sysinfo ">=0.32,<=0.40"

# Relax dependency for sqlx
tomcli set crates/goose/Cargo.toml str dependencies.sqlx ">=0.7,<=0.9"

# Relax dependency for rustyline
tomcli set crates/goose-cli/Cargo.toml str dependencies.rustyline ">=14.0.0,<=16.0.0"

# Relax dependency for mockall
tomcli set crates/goose/Cargo.toml str dependencies.mockall ">=0.13.1,<=0.14.0"

# Relax dependency for minijinja
tomcli set crates/goose/Cargo.toml str dependencies.minijinja ">=2.10.2,<=3.0.0"

# Relax dependency for lopdf
tomcli set crates/goose-mcp/Cargo.toml str dependencies.lopdf ">=0.35.0,<=0.37.0"

# Relax dependency for indicatif
tomcli set crates/goose-cli/Cargo.toml str dependencies.indicatif ">=0.16.2,<=0.19.0"

# Relax dependency for ignore
tomcli set crates/goose-mcp/Cargo.toml str dependencies.ignore ">=0.4.0,<=0.5.0"

# Relax dependency for etcetera
tomcli set crates/goose-mcp/Cargo.toml str dependencies.etcetera ">=0.8.0,<=0.12.0"

# Relax dependency for dirs
tomcli set crates/goose/Cargo.toml str dependencies.dirs ">=5.0.0,<=6.0.0"

# Remove criterion as it is a benchmark only dependency
tomcli set crates/goose/Cargo.toml del dev-dependencies.criterion

# Relax dependency for console
tomcli set crates/goose-cli/Cargo.toml str dependencies.console ">=0.15.8,<=0.17.0"

# Relax dependency for console
tomcli set crates/goose-server/Cargo.toml str dependencies.config ">=0.14.1,<=0.16.0"

# Relax dependency for bat
tomcli set crates/goose-cli/Cargo.toml str dependencies.bat ">=0.24.0,<=0.27.0"

# Remove unused dependencies
# Based on https://github.com/block/goose/pull/6380/changes
tomcli set crates/goose-cli/Cargo.toml del "dependencies.agent-client-protocol-schema"
tomcli set crates/goose-cli/Cargo.toml del "dependencies.is-terminal"
tomcli set crates/goose-cli/Cargo.toml del "dependencies.jsonschema"

tomcli set crates/goose-mcp/Cargo.toml del "dependencies.http-body-util"
tomcli set crates/goose-mcp/Cargo.toml del "dependencies.keyring"
tomcli set crates/goose-mcp/Cargo.toml del "dependencies.oauth2"
tomcli set crates/goose-mcp/Cargo.toml del "dependencies.hyper"
tomcli set crates/goose-mcp/Cargo.toml del "dependencies.serde_with"
tomcli set crates/goose-mcp/Cargo.toml del "dependencies.streaming-iterator"
tomcli set crates/goose-mcp/Cargo.toml del "dependencies.clap"

tomcli set crates/goose/Cargo.toml del "dev-dependencies.agent-client-protocol-schema"
tomcli set crates/goose/Cargo.toml del "dependencies.tonic"
tomcli set crates/goose/Cargo.toml lists delitem "dependencies.opentelemetry-otlp.features" "grpc-tonic"
tomcli set crates/goose/Cargo.toml del "dependencies.oauth2"
tomcli set crates/goose/Cargo.toml del "dependencies.boa_gc"

%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires -t

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
install -Dpm 0755 target/rpm/goose -t %{buildroot}%{_bindir}
install -Dpm 0755 target/rpm/goosed -t %{buildroot}%{_bindir}

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/goose
%{_bindir}/goosed

%changelog
%autochangelog
