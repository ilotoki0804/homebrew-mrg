class Mrg < Formula
  include Language::Python::Virtualenv

  desc "Clean miscellaneous files produced by macOS"
  homepage "https://github.com/ilotoki0804/mrg"
  url "https://files.pythonhosted.org/packages/source/m/mrg/mrg-0.1.0.post4.tar.gz"
  sha256 "da98b99ba89b59e51263e5dd728e7fe273d56f4a675d6b97c8a4eeab68570112"
  license "Apache-2.0"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
  end

  test do
    (testpath/"sample").mkpath
    (testpath/"sample"/".DS_Store").write("")

    output = shell_output("#{bin}/mrg #{testpath}/sample --ds-store --json")
    assert_match '"ds_store": 1', output
    assert_match '"ds_store_fixed": true', output
    refute_predicate testpath/"sample"/".DS_Store", :exist?
  end
end
