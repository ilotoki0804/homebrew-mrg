class Mrg < Formula
  include Language::Python::Virtualenv

  desc "Clean miscellaneous files produced by macOS"
  homepage "https://github.com/ilotoki0804/mrg"
  url "https://files.pythonhosted.org/packages/source/m/mrg/mrg-0.2.0.tar.gz"
  sha256 "6e4016828cb966df4de183777a69dfdc9234bc0998028f1b048f207ee12d92d8"
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
