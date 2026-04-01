class Tamagotchi < Formula
  include Language::Python::Virtualenv

  desc "Terminal virtual pet — raise a Tamagotchi in your CLI"
  homepage "https://github.com/usik/tamagotchi"
  url "https://files.pythonhosted.org/packages/source/t/tamagotchi/tamagotchi-0.1.0.tar.gz"
  # Update sha256 after first PyPI publish:
  # sha256 "REPLACE_AFTER_PYPI_PUBLISH"
  license "MIT"
  head "https://github.com/usik/tamagotchi.git", branch: "main"

  depends_on "python@3.12"

  resource "textual" do
    url "https://files.pythonhosted.org/packages/source/t/textual/textual-0.70.0.tar.gz"
    sha256 "" # filled in by `brew audit --new`
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.7.0.tar.gz"
    sha256 ""
  end

  resource "pydantic" do
    url "https://files.pythonhosted.org/packages/source/p/pydantic/pydantic-2.7.0.tar.gz"
    sha256 ""
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "0.1.0", shell_output("#{bin}/tama --version")
  end
end
